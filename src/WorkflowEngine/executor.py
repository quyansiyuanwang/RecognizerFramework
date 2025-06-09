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

from src.Typehints import GlobalsDict, TaskAttemptDict
from src.Typehints.workflow import IdentifiedGlobalsDict
from src.WorkflowEngine.Controller import LogController

from ..Structure import Job, Limits
from .Controller import global_log_manager
from .exceptions import NeededError, RetryError
from .manager import WorkflowManager

LogLevel = LogController.LogLevel


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

    def execute(self) -> _EXEC_YT:
        if self.job["type"] in self.executors:
            executor_class = self.executors[self.job["type"]]
            executor_instance = executor_class(self.job, self.globals)
            return executor_instance.execute(job=self.job)
        else:
            raise ValueError(f"Unknown job type: {self.job['type']}")

    def __call__(self) -> Any:
        return self.execute()


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
        self.globals_: IdentifiedGlobalsDict = workflow.get_globals(
            IdentifiedGlobalsDict()
        )

        # logger setup
        self.global_log_manager: LogController.LogManager = global_log_manager
        self.global_log_manager.set_level_str(self.globals_.get("logLevel", "LOG"))
        self.global_log_manager.set_debug(self.globals_.get("debug", False))

    def set_callback(self, callback: Callable[..., Any]) -> None:
        self.callback = callback

    def check_needed(
        self, job: Job, needs: Optional[List[str]], results: Dict[str, _EXEC_YT]
    ) -> Union[NoReturn, None]:
        if needs is None or all(name in results for name in needs):
            return None
        missing: List[str] = [name for name in needs if name not in results]
        raise NeededError(
            job,
            f"Not all needed tasks are completed. Missing: {missing}. "
            f"Available results: {list(results.keys())}",
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
            {"maxCount": -1, "maxFailure": -1, "maxSuccess": -1}
        )

    def _log_event(self, event: str, **kwargs: Any):
        templates = {
            "TaskStatus": (
                "Current try: {attempts} for job '{job_name}'({limits})",
                [LogLevel.WARNING, LogLevel.DEBUG],
            ),
            "JobResult": (
                "Job '{job_name}' Execute {result}",
                [
                    LogLevel.INFO if kwargs.get("success") else LogLevel.ERROR,
                    LogLevel.DEBUG,
                ],
            ),
            "NextJob": (
                "Directing to next job: '{nxt_job}' after job '{cur_job}'",
                [LogLevel.INFO, LogLevel.DEBUG],
            ),
            "Error": (
                "Error in job '{job_name}': {error}.",
                [LogLevel.ERROR, LogLevel.DEBUG],
            ),
        }
        if event not in templates:
            assert False, f"Unknown event type: {event}"
        fmt, levels = templates[event]

        if event == "JobResult":
            kwargs = dict(kwargs)
            kwargs["result"] = "success" if kwargs.get("success") else "failure"

        global_log_manager.log(
            fmt.format(**kwargs),
            levels,
            debug=self.globals_.get("debug", False),
            log_config=self.globals_.get("logConfig"),
        )

    def run(self) -> Generator[_EXEC_YT, _EXEC_ST, List[_CB_SF_V]]:
        results: Dict[str, _EXEC_YT] = {}
        cur_job_name: str = self.workflow.get_begin()
        while cur_job_name in self.workflow:
            # var init
            job: Optional[Job] = self.workflow.get_job(cur_job_name)
            # early return
            if job is None:
                return [self.callback(result) for result in results.values()]
            success: bool = True
            attempts: TaskAttemptDict = self._get_task_attempts(cur_job_name, 0)
            limits: Limits = self._get_task_limits(job)
            # legal check
            self.check_attempts(job, attempts, limits)
            # log event
            self._log_event(
                event="TaskStatus",
                job_name=cur_job_name,
                attempts=sum(v for v in attempts.values() if isinstance(v, int)) + 1,
                limits=limits,
            )
            try:
                # legal check
                self.check_needed(job, needs=job["needs"], results=results)
                # exec
                result: _EXEC_YT = JobExecutor[_EXEC_YT, _EXEC_ST, _EXEC_RT](
                    job=job, globals=self.workflow.get_globals({})
                ).execute()
                # record results
                results[cur_job_name] = result
                attempts["success"] += 1
                self._tries[cur_job_name] = attempts
                yield result
            except NeededError as e:
                raise NeededError(
                    job=job,
                    message=f"Missing dependencies for task '{cur_job_name}': {e}",
                ) from e
            except Exception as e:
                # handle error
                success = False
                attempts["failure"] += 1
                self._tries[cur_job_name] = attempts
                self._log_event("Error", job_name=cur_job_name, error=e)
            finally:
                nxt = self.workflow.get_next(cur_job_name, success) or ""
                # log event
                self._log_event(
                    "NextJob",
                    nxt_job=nxt,
                    cur_job=cur_job_name,
                )
                self._log_event("JobResult", job_name=cur_job_name, success=success)

            cur_job_name = nxt

        return [self.callback(result) for result in results.values()]

    def await_run_all(self) -> List[_CB_SF_V]:
        results: List[_CB_SF_V] = []
        for result in self.run():
            results.append(self.callback(result))
        return results
