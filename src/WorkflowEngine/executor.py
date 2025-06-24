import importlib
import os
from abc import ABC, abstractmethod
from collections.abc import Generator
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    List,
    Literal,
    NoReturn,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from ..Structure import Delay, Job, Limits
from ..Typehints import AfterDict, GlobalsDict, IdentifiedGlobalsDict, TaskAttemptDict
from ..WorkflowEngine.Exceptions.base import (
    CrashException,
    CriticalException,
    IgnorableError,
)
from ..WorkflowEngine.Exceptions.crash import (
    JobNotFoundError,
    JobTypeError,
    NeededError,
)
from ..WorkflowEngine.Exceptions.critical import RetryError
from .Controller import LogController, LogLevel, global_log_manager
from .Exceptions.ignorable import AfterJobRunError
from .manager import WorkflowManager
from .Util.executor_works import delay as task_delay


class Executor(ABC):

    @abstractmethod
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass


_EXEC_YT = TypeVar("_EXEC_YT")
_EXEC_ST = TypeVar("_EXEC_ST", bound=None, default=None)
_EXEC_RT = TypeVar("_EXEC_RT", bound=None, default=None)


class JobExecutor(Generic[_EXEC_YT, _EXEC_ST, _EXEC_RT]):
    executors: Dict[str, Type[Executor]] = {}

    def __init__(self, job: Job, globals: Optional[GlobalsDict] = None) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals if globals is not None else {}

    @staticmethod
    def import_trigger(module_path: str):
        dir_path = module_path.replace(".", os.sep)
        if os.path.isdir(dir_path):
            for filename in os.listdir(dir_path):
                if filename.endswith(".py") and not filename.startswith("__"):
                    module_name = filename[:-3]
                    full_module_path = f"{module_path}.{module_name}"
                    try:
                        importlib.import_module(full_module_path)
                    except Exception as e:
                        raise ImportError(
                            f"Failed to import module '{full_module_path}': {e}"
                        ) from e
        else:
            try:
                importlib.import_module(module_path)
            except Exception as e:
                raise ImportError(
                    f"Failed to import module '{module_path}': {e}"
                ) from e

    @classmethod
    def register(cls, name: str) -> Callable[..., type[Executor]]:
        def decorator(executor: Union[Type[Executor], Any]) -> type[Executor]:
            if not issubclass(executor, Executor):
                raise TypeError(f"{name} must be a subclass of Executor")
            cls.executors[name] = executor
            return executor

        return decorator

    def execute(self, *args: Any, **kwargs: Any) -> _EXEC_YT:
        if self.job["type"] in self.executors:
            executor_class = self.executors[self.job["type"]]
            executor_instance = executor_class(self.job, self.globals)
            return executor_instance.execute(*args, **kwargs)
        else:
            raise JobTypeError(f"Unknown job type: {self.job['type']}")

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.execute(*args, **kwargs)


_CB_SF_V = TypeVar("_CB_SF_V", bound=Any, default=None)


class ExecutorManager(Generic[_EXEC_YT, _EXEC_ST, _EXEC_RT, _CB_SF_V]):
    @staticmethod
    def __self_callback(args: _CB_SF_V) -> _CB_SF_V:
        return args

    def __init__(
        self,
        workflow: WorkflowManager,
        callback: Callable[..., Any] = __self_callback,
    ) -> None:
        self.workflow: WorkflowManager = workflow
        self._tries: Dict[str, TaskAttemptDict] = {}
        self.callback: Union[
            Callable[..., Any], Callable[[Union[_EXEC_YT, _CB_SF_V]], _CB_SF_V]
        ] = callback
        self.globals: IdentifiedGlobalsDict = workflow.get_globals(
            IdentifiedGlobalsDict()
        )

        # logger setup
        self.global_log_manager: LogController.LogManager = global_log_manager
        self.global_log_manager.set_level_str(self.globals.get("logLevel", "LOG"))
        self.global_log_manager.set_debug(self.globals.get("debug", False))
        self.global_log_manager.set_attr(self.globals)

        # global flag
        self.crashed: bool = False

    def set_callback(self, callback: Callable[..., Any]) -> None:
        self.callback = callback

    def check_needed(
        self, job: Job, needs: Optional[List[str]], results: Dict[str, _EXEC_YT]
    ) -> Union[NoReturn, None]:
        if needs is None or all(name in results for name in needs):
            return None
        missing: List[str] = [name for name in needs if name not in results]
        raise NeededError(
            f"Not all needed tasks are completed. Missing: {missing}. "
            f"Available results: {list(results.keys())}",
            job=job,
        )

    def check_attempts(
        self, job: Job, ta: TaskAttemptDict, tl: Limits
    ) -> Union[NoReturn, None]:
        limits: List[
            Tuple[Literal["maxCount", "maxFailure", "maxSuccess"], int, str]
        ] = [
            ("maxCount", ta.get("success", 0) + ta.get("failure", 0), "attempts"),
            ("maxFailure", ta.get("failure", 0), "failures"),
            ("maxSuccess", ta.get("success", 0), "successes"),
        ]
        for key, value, label in limits:
            max_limit: int = tl.get(key, -1)
            if max_limit != -1 and value >= max_limit:
                raise RetryError(
                    job=job,
                    message=f"Task '{job.get('name')}' exceeded {key}: {max_limit} {label}",
                )
        return None

    def _get_task_attempts(self, job_name: str, start: int) -> TaskAttemptDict:
        return self._tries.get(job_name) or TaskAttemptDict(
            success=start, failure=start
        )

    def _get_task_limits(self, job: Job) -> Limits:
        return job.get("limits") or Limits(
            kwargs={"maxCount": -1, "maxFailure": -1, "maxSuccess": -1, "exit": None}
        )

    def _log_event(self, event: str, **kwargs: Any):
        templates = {
            "TaskStatus": (
                "Current try: {attempts} for job '{job_name}'({limits})",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "JobResult": (
                "Job '{job_name}' Execute {result}",
                (
                    [LogLevel.INFO, LogLevel.DEBUG]
                    if kwargs.get("success")
                    else [LogLevel.WARNING, LogLevel.DEBUG]
                ),
            ),
            "NextJob": (
                "Directing to next job: '{nxt_job}' after job '{cur_job}'",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "MaxAttemptsForExit": (
                "Max attempts reached for job '{job_name}': {attempts}. "
                "Exiting workflow.",
                [LogLevel.ERROR],
            ),
            "MaxAttemptsForSwitch": (
                "Max attempts reached for job '{job_name}': {attempts}. "
                "Switching to job '{exit_job}'.",
                [LogLevel.WARNING, LogLevel.DEBUG],
            ),
            "Error": (
                "Error in job '{job_name}': {error}.",
                [LogLevel.ERROR],
            ),
            "Warn": (
                "Warning in job '{job_name}': {error}.",
                [LogLevel.WARNING],
            ),
            "JobsCompletion": (
                "All jobs completed successfully. Jobs Chain: {jobs_chain}",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "AfterJobTip": (
                "After '{job_name}' job run: '{aft_job}'",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "AfterJobResult": (
                "After job '{job_name}' Execute {result}",
                (
                    [LogLevel.INFO, LogLevel.DEBUG]
                    if kwargs.get("success")
                    else [LogLevel.WARNING, LogLevel.DEBUG]
                ),
            ),
            "Crash": (
                "Crash occurred in job '{job_name}': {error}",
                [LogLevel.CRITICAL],
            ),
        }
        if event not in templates:
            assert False, f"Unknown event type: {event}"
        fmt, levels = templates[event]

        if event in {"JobResult", "AfterJobResult"}:
            kwargs = dict(kwargs)
            kwargs["result"] = "success" if kwargs.get("success") else "failure"

        global_log_manager.log(
            fmt.format(**kwargs),
            levels,
            debug=self.globals.get("debug", False),
            log_config=self.globals.get("logConfig"),
        )

    def _after_run(self, job: Job, run_status: bool) -> None:
        after: Optional[AfterDict] = job.get("after", None)
        if after is None:
            return
        ignore: bool = after.get("ignore_errors", False)
        always: List[str] = after.get("always", [])
        executed: Set[str] = set()
        tasks: List[str] = always + (
            after.get("success", []) if run_status else after.get("failure", [])
        )
        for task in tasks:
            if task in executed:
                continue

            aft_job = self.workflow.get_job(task)
            if aft_job is None:
                raise JobNotFoundError(f"Job '{task}' not found in workflow.")

            executed.add(aft_job.get("name"))
            self._log_event(
                "AfterJobTip", job_name=job.get("name"), aft_job=aft_job.get("name")
            )

            try:
                JobExecutor[_EXEC_YT, _EXEC_ST, _EXEC_RT](aft_job).execute()
            except IgnorableError as e:
                if not ignore:
                    raise AfterJobRunError(job=aft_job, message=str(e)) from e
            except CrashException as e:
                self._log_event("Error", job_name=task, error=e)
                raise CrashException("Crash occurred", aft_job) from e
            finally:
                self._log_event("AfterJobResult", job_name=task, success=True)

    def __pre_works(
        self, *_: Any, job: Job, globals: IdentifiedGlobalsDict, **kwargs: Any
    ) -> None:
        # delay
        delay: Optional[Delay] = job.get("delay", None)
        if delay is not None:
            task_delay(delay, mode="pre", globals=globals, **kwargs)

    def __post_works(
        self, *_: Any, job: Job, globals: IdentifiedGlobalsDict, **kwargs: Any
    ) -> None:
        # delay
        delay: Optional[Delay] = job.get("delay", None)
        if delay is not None:
            task_delay(delay, mode="post", globals=globals, **kwargs)

    def run(self) -> Generator[_EXEC_YT, _EXEC_ST, List[_CB_SF_V]]:
        results: Dict[str, _EXEC_YT] = {}
        cur_job_name: str = self.workflow.get_begin()
        work_chain: List[str] = []
        while cur_job_name in self.workflow:
            # var init
            job: Optional[Job] = self.workflow.get_job(cur_job_name)
            if job is None:  # early return
                return [self.callback(result) for result in results.values()]
            success: bool = False
            attempts: TaskAttemptDict = self._get_task_attempts(cur_job_name, 0)
            limits: Limits = self._get_task_limits(job)

            # log event
            self._log_event(
                event="TaskStatus",
                job_name=cur_job_name,
                attempts=sum(v for v in attempts.values() if isinstance(v, int)) + 1,
                limits=limits,
            )
            try:
                # legal check
                self.check_attempts(job, attempts, limits)
                self.check_needed(job, needs=job["needs"], results=results)

                # exec
                self.__pre_works(job=job, globals=self.globals, prefix=job["type"])
                result: _EXEC_YT = JobExecutor[_EXEC_YT, _EXEC_ST, _EXEC_RT](
                    job=job, globals=self.workflow.get_globals({})
                ).execute()

                # record results
                results[cur_job_name] = result
                attempts["success"] += 1
                self._tries[cur_job_name] = attempts
                work_chain.append(cur_job_name)
                success = True
                yield result

            except IgnorableError as e:
                # handle error
                attempts["failure"] += 1
                self._tries[cur_job_name] = attempts
                self._log_event("Warn", job_name=cur_job_name, error=e)

            except CriticalException as e:
                exit_job: Optional[str] = limits.get("exit")
                if exit_job is None:
                    self._log_event(
                        "MaxAttemptsForExit",
                        job_name=cur_job_name,
                        attempts=attempts.get("success", 0)
                        + attempts.get("failure", 0),
                    )
                    self.crashed = True
                    raise CrashException(
                        f"Critical exception in job '{cur_job_name}': {e.message}",
                        job=job,
                    ) from e
                self._log_event(
                    "MaxAttemptsForSwitch",
                    job_name=cur_job_name,
                    attempts=attempts.get("success", 0) + attempts.get("failure", 0),
                    exit_job=exit_job,
                )
                if self.workflow.get_job(exit_job) is None:
                    raise JobNotFoundError(f"Exit job '{exit_job}' not found.")
                self._log_event(
                    "NextJob",
                    nxt_job=exit_job,
                    cur_job=cur_job_name,
                )
                cur_job_name = exit_job
                continue

            except CrashException as e:
                self._log_event("Crash", job_name=cur_job_name, error=e)
                self.crashed = True
                raise CrashException(
                    f"Crash occurred in job '{cur_job_name}': {e.message}",
                    job=job,
                ) from e

            finally:
                if not self.crashed:
                    self._after_run(
                        job=job,
                        run_status=success,
                    )
                    self.__post_works(job=job, globals=self.globals, prefix=job["type"])

            nxt = self.workflow.get_next(cur_job_name, success)
            # log event
            self._log_event("JobResult", job_name=cur_job_name, success=success)
            if nxt is None:
                self._log_event(
                    "JobsCompletion",
                    jobs_chain=" -> ".join(work_chain),
                )
                break
            self._log_event(
                "NextJob",
                nxt_job=nxt,
                cur_job=cur_job_name,
            )

            cur_job_name = nxt

        return [self.callback(result) for result in results.values()]

    def await_run_all(self) -> List[_CB_SF_V]:
        results: List[_CB_SF_V] = []
        for result in self.run():
            results.append(self.callback(result))
        return results
