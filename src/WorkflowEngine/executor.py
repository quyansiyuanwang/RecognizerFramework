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
    Tuple,
    Type,
    TypeVar,
    Union,
)

from ..Structure import Delay, Job, Limits, Use
from ..Typehints import (
    AfterDict,
    BeforeDict,
    GlobalsDict,
    IdentifiedGlobalsDict,
    TaskAttemptDict,
    TaskReturnsDict,
)
from ..WorkflowEngine.Exceptions.base import (
    CrashException,
    CriticalException,
    IgnorableError,
)
from ..WorkflowEngine.Exceptions.crash import (
    JobNotFoundError,
    JobTypeError,
    MissingRequiredError,
    NeededError,
)
from ..WorkflowEngine.Exceptions.critical import RetryError
from .Controller import LogController, LogLevel, global_log_manager
from .Exceptions.ignorable import AfterJobRunError, BeforeJobRunError
from .manager import WorkflowManager
from .Util.executor_works import delay as task_delay


class Executor(ABC):

    @abstractmethod
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[Any]:
        pass


"""Generic TypeVars"""
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

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[_EXEC_YT]:
        if self.job["type"] in self.executors:
            executor_class = self.executors[self.job["type"]]
            executor_instance = executor_class(self.job, self.globals)
            ret: TaskReturnsDict[_EXEC_YT] = executor_instance.execute(*args, **kwargs)

            returns: Dict[str, str] = ret["returns"]
            variables: Dict[str, Any] = ret["variables"]
            for key, value in returns.items():
                if value in variables:
                    returns[key] = variables[value]
                else:
                    raise MissingRequiredError(
                        job=self.job,
                        message=f"Missing required return variable: {value}",
                    )

            return TaskReturnsDict[_EXEC_YT](
                result=ret["result"], returns=returns, variables=variables
            )
        else:
            raise JobTypeError(f"Unknown job type: {self.job['type']}")

    def __call__(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[_EXEC_YT]:
        return self.execute(*args, **kwargs)


_CB_SF_V = TypeVar("_CB_SF_V", bound=Any, default=None)


class ExecutorManager(Generic[_EXEC_YT, _EXEC_ST, _EXEC_RT, _CB_SF_V]):
    __JOB_RESULT_MAP: Dict[bool, str] = {
        True: "Success",
        False: "Failure",
    }

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
        self.run_status: bool = False
        self.success: bool = False

        # global job instance & variables init
        self.cur_job_name: str = self.workflow.get_begin()
        cur_job: Optional[Job] = self.workflow.get_job(self.cur_job_name or "")
        if cur_job is None:
            raise JobNotFoundError(f"Job '{self.cur_job_name}' not found in workflow.")
        self.cur_job: Job = cur_job

        # global instance & variables below
        self.task_vars: Dict[str, Dict[str, Any]] = {}
        self.results: Dict[str, TaskReturnsDict[_EXEC_YT]] = {}
        self.work_chain: List[str] = []
        self.load_params()

    def load_params(self):
        self.attempts: TaskAttemptDict = self._get_task_attempts(self.cur_job_name, 0)
        self.limits: Limits = self._get_task_limits(self.cur_job)
        self.use: Use = self.cur_job.get("use", {})

    def set_callback(self, callback: Callable[..., Any]) -> None:
        self.callback = callback

    def switch_next_job(self) -> Optional[Job]:
        """Switch to the next job in the workflow.

        Raises:
            JobNotFoundError: If the next job is not found in the workflow.

        Returns:
            Job: The next job in the workflow.
        """
        self._log_event(
            "JobResult",
            job_name=self.cur_job_name,
            result=ExecutorManager.__JOB_RESULT_MAP.get(self.success),
        )
        nxt = self.workflow.get_next(self.cur_job_name, self.success)
        nxt_job = self.workflow.get_job(nxt or "")
        if nxt is None or nxt_job is None:
            return None
        self.cur_job_name = nxt
        self.cur_job = nxt_job

        self.load_params()

        self._log_event(
            event="TaskStatus",
            job_name=self.cur_job_name,
            attempts=sum(v for v in self.attempts.values() if isinstance(v, int)) + 1,
            limits=self.limits,
        )
        self._log_event(
            "NextJob",
            nxt_job=nxt,
            cur_job=self.cur_job_name,
        )
        return nxt_job

    def switch_exit_job(self) -> Optional[Job]:
        """Call the function means the task reached max attempts for exit.

        Returns:
            Optional[Job]: The exit job if it exists, otherwise None.
        """
        exit_job_name: Optional[str] = self.cur_job.get("limits", {}).get("exit")
        exit_job = self.workflow.get_job(self.cur_job_name)
        if exit_job_name is None or exit_job is None:
            self.crashed = True
            self._log_event(
                "MaxAttemptsForExit",
                job_name=self.cur_job_name,
                attempts=self.attempts.get("success", 0)
                + self.attempts.get("failure", 0),
            )
            return None
        self.cur_job_name = exit_job_name
        self.cur_job = exit_job
        self._log_event(
            "MaxAttemptsForSwitch",
            job_name=self.cur_job_name,
            attempts=self.attempts.get("success", 0) + self.attempts.get("failure", 0),
            exit_job=exit_job,
        )

        return exit_job

    def check_needed(self, job: Job) -> Union[NoReturn, None]:
        needs = job.get("needs", None)
        if needs is None or all(name in self.results for name in needs):
            return None
        missing: List[str] = [name for name in needs if name not in self.results]
        raise NeededError(
            f"Not all needed tasks are completed. Missing: {missing}. "
            f"Available results: {list(self.results.keys())}",
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
                ([LogLevel.INFO if self.success else LogLevel.WARNING, LogLevel.DEBUG]),
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
            "BeforeJobTip": (
                "Before '{job_name}' job run: '{bef_job}'",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "BeforeJobResult": (
                "Before job '{job_name}' Execute {result}",
                ([LogLevel.INFO if self.success else LogLevel.WARNING, LogLevel.DEBUG]),
            ),
            "AfterJobTip": (
                "After '{job_name}' job run: '{aft_job}'",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "AfterJobResult": (
                "After job '{job_name}' Execute {result}",
                ([LogLevel.INFO if self.success else LogLevel.WARNING, LogLevel.DEBUG]),
            ),
            "Crash": (
                "Crash occurred in job '{job_name}': {error}",
                [LogLevel.CRITICAL],
            ),
        }
        if event not in templates:
            assert False, f"Unknown event type: {event}"
        fmt, levels = templates[event]

        global_log_manager.log(
            fmt.format(**kwargs),
            levels,
            debug=self.globals.get("debug", False),
            log_config=self.globals.get("logConfig"),
        )

    def _before_run(self, job: Job) -> None:
        before: Optional[BeforeDict] = job.get("before", None)
        if before is None:
            return
        ignore: bool = before.get("ignore_errors", False)
        tasks: List[str] = before.get("tasks", [])
        for task in tasks:
            bef_job = self.workflow.get_job(task)
            if bef_job is None:
                raise JobNotFoundError(f"Job '{task}' not found in workflow.")

            self._log_event(
                "BeforeJobTip", job_name=job.get("name"), bef_job=bef_job.get("name")
            )
            success = False
            try:
                self.check_needed(bef_job)

                self.__pre_works(job=bef_job)
                self._before_run(job=bef_job)

                self.results[task] = JobExecutor[_EXEC_YT, _EXEC_ST, _EXEC_RT](
                    bef_job
                ).execute()
                success = True
            except IgnorableError as e:
                if not ignore:
                    raise BeforeJobRunError(job=bef_job, message=str(e)) from e

            except CrashException as e:
                self._log_event("Error", job_name=task, error=e)
                raise CrashException("Crash occurred", bef_job) from e
            finally:
                self._log_event(
                    "BeforeJobResult",
                    job_name=task,
                    result=ExecutorManager.__JOB_RESULT_MAP.get(success),
                )
            if not self.crashed:
                self._after_run(job=bef_job)
                self.__post_works(job=bef_job)

    def _after_run(self, job: Job) -> None:
        after: Optional[AfterDict] = job.get("after", None)
        if after is None:
            return
        ignore: bool = after.get("ignore_errors", False)
        always: List[str] = after.get("always", [])
        tasks: List[str] = always + (
            after.get("success", []) if self.success else after.get("failure", [])
        )
        for task in tasks:
            aft_job = self.workflow.get_job(task)
            if aft_job is None:
                raise JobNotFoundError(f"Job '{task}' not found in workflow.")

            self._log_event(
                "AfterJobTip", job_name=job.get("name"), aft_job=aft_job.get("name")
            )
            success = False
            try:
                self.check_needed(aft_job)

                self.__pre_works(job=aft_job)
                self._before_run(job=aft_job)

                self.results[task] = JobExecutor[_EXEC_YT, _EXEC_ST, _EXEC_RT](
                    aft_job
                ).execute()
                success = True
            except IgnorableError as e:
                if not ignore:
                    raise AfterJobRunError(job=aft_job, message=str(e)) from e
            except CrashException as e:
                self._log_event("Error", job_name=task, error=e)
                raise CrashException("Crash occurred", aft_job) from e
            finally:
                self._log_event(
                    "AfterJobResult",
                    job_name=task,
                    result=ExecutorManager.__JOB_RESULT_MAP.get(success),
                )
            if not self.crashed:
                self._after_run(job=aft_job)
                self.__post_works(job=aft_job)

    def __pre_works(self, *_: Any, job: Job) -> None:
        jn = job.get("name", None)
        self.work_chain.append(jn)

        # delay
        delay: Optional[Delay] = job.get("delay", None)
        if delay is not None:
            task_delay(delay, mode="pre", globals=self.globals, prefix=job["type"])

    def __post_works(self, *_: Any, job: Job) -> None:
        # delay
        delay: Optional[Delay] = job.get("delay", None)
        if delay is not None:
            task_delay(delay, mode="post", globals=self.globals, prefix=job["type"])

    def run(self) -> Generator[_EXEC_YT, _EXEC_ST, List[_CB_SF_V]]:
        self.run_status = True
        while self.run_status:
            self.success = False
            use_vars: Dict[str, Any] = self.task_vars.get(self.cur_job.get("use"), {})

            try:
                # legal check
                self.check_attempts(job=self.cur_job, ta=self.attempts, tl=self.limits)
                self.check_needed(job=self.cur_job)

                # exec
                self.__pre_works(job=self.cur_job)
                self._before_run(job=self.cur_job)

                result: TaskReturnsDict[_EXEC_YT] = JobExecutor[
                    _EXEC_YT, _EXEC_ST, _EXEC_RT
                ](job=self.cur_job, globals=self.workflow.get_globals({})).execute(
                    **use_vars
                )
                # record results
                self.success = True
                self.results[self.cur_job_name] = result
                self.task_vars[self.cur_job_name] = result["returns"]
                self.attempts["success"] += 1
                self._tries[self.cur_job_name] = self.attempts
                yield result["result"]

            except IgnorableError as e:
                # handle error
                self.attempts["failure"] += 1
                self._tries[self.cur_job_name] = self.attempts
                self._log_event("Warn", job_name=self.cur_job_name, error=e)

            except CriticalException as e:
                if self.switch_exit_job() is None:
                    raise CrashException(
                        f"Critical exception in job '{self.cur_job_name}': {e.message}",
                        job=self.cur_job,
                    ) from e
                continue

            except CrashException as e:
                self._log_event("Crash", job_name=self.cur_job_name, error=e)
                self.crashed = True
                self.run_status = False
                raise CrashException(
                    f"Crash occurred in job '{self.cur_job_name}': {e.message}",
                    job=self.cur_job,
                ) from e

            finally:
                if not self.crashed:
                    self._after_run(job=self.cur_job)
                    self.__post_works(job=self.cur_job)

            if self.switch_next_job() is None:
                break

        return [self.callback(result["result"]) for result in self.results.values()]

    def await_run_all(self) -> List[_CB_SF_V]:
        results: List[_CB_SF_V] = []
        for result in self.run():
            results.append(self.callback(result))
        return results
