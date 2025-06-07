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
    NoReturn,
    Optional,
    Type,
    TypeVar,
    Union,
)

from src.Typehints import GlobalsDict
from src.WorkflowEngine.Controller import LogController

from ..Structure import Job
from .exceptions import NeededError, RetryError
from .manager import WorkflowManager

Logger = LogController.Logger
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

    def __init__(
        self, name: str, job: Job, globals: Optional[GlobalsDict] = None
    ) -> None:
        self.name: str = name
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
        self._tries: Dict[str, int] = {}
        self.callback: Union[
            Callable[..., Any], Callable[[Union[_EXEC_YT, _CB_SF_V]], _CB_SF_V]
        ] = callback

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

    def run(self) -> Generator[_EXEC_YT, _EXEC_ST, List[_CB_SF_V]]:
        results: Dict[str, _EXEC_YT] = {}
        cur_job_name: str = self.workflow.get_begin()
        globals_: GlobalsDict = self.workflow.get_globals() or {}
        while cur_job_name in self.workflow:
            job: Optional[Job] = self.workflow.get_job(cur_job_name)
            if job is None:
                return [self.callback(result) for result in results.values()]
            success: bool = True
            if globals_.get("debug", False):
                Logger.log(
                    f"Current try: {self._tries.get(cur_job_name, 1)} for job '{cur_job_name}'(max: {job.get('maxTries', -1)})",
                    [LogLevel.WARNING, LogLevel.DEBUG],
                )
            try:
                self.check_needed(job, needs=job["needs"], results=results)

                result: _EXEC_YT = JobExecutor[_EXEC_YT](
                    name=cur_job_name, job=job, globals=self.workflow.get_globals()
                ).execute()
                results[cur_job_name] = result
                yield result
            except NeededError as e:
                raise NeededError(
                    job=job,
                    message=f"Missing dependencies for task '{cur_job_name}': {e}",
                ) from e
            except Exception as e:
                success = False
                self._tries[cur_job_name] = self._tries.get(cur_job_name, 0) + 1
                if globals_.get("debug", False):
                    Logger.log(
                        f"Error in job '{cur_job_name}': {e}. ",
                        [LogLevel.ERROR, LogLevel.DEBUG],
                    )
            finally:
                if self._tries.get(cur_job_name, 0) == job.get("maxTries", -1):
                    raise RetryError(
                        job=job,
                        message=f"Task '{cur_job_name}' failed after {self._tries[cur_job_name]} tries",
                    )
                original_job_name = cur_job_name
                cur_job_name = self.workflow.get_next(cur_job_name, success) or ""
                if globals_.get("debug", False):
                    Logger.log(
                        f"Job '{cur_job_name}' Execute {{'success' if success else 'failure'}}",
                        [
                            LogLevel.INFO if success else LogLevel.ERROR,
                            LogLevel.DEBUG,
                        ],
                    )
                    Logger.log(
                        f"Directing to next job: '{cur_job_name}' after job '{original_job_name}'",
                        [LogLevel.INFO, LogLevel.DEBUG],
                    )

        return [self.callback(result) for result in results.values()]

    def await_run_all(self) -> List[_CB_SF_V]:
        results: List[_CB_SF_V] = []
        for result in self.run():
            results.append(self.callback(result))
        return results
