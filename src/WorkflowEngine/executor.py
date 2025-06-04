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

from ..Structure import Job
from .manager import WorkflowManager


class Executor(ABC):

    @abstractmethod
    def __init__(self, job: Job) -> None:
        pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        pass


_EXEC_YT = TypeVar("_EXEC_YT")
_EXEC_ST = TypeVar("_EXEC_ST", bound=None, default=None)
_EXEC_RT = TypeVar("_EXEC_RT", bound=None, default=None)


class JobExecutor(Generic[_EXEC_YT, _EXEC_ST, _EXEC_RT]):
    executors: Dict[str, Type[Executor]] = {}

    def __init__(self, name: str, job: Job):
        self.name: str = name
        self.job: Job = job

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
            executor_instance = executor_class(self.job)
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
        workflow: Optional[WorkflowManager] = None,
        callback: Callable[..., Any] = __self_callback,
    ) -> None:
        self.tasks: List[JobExecutor[_EXEC_YT, _EXEC_ST, _EXEC_RT]] = []
        self.callback: Union[
            Callable[..., Any], Callable[[Union[_EXEC_YT, _CB_SF_V]], _CB_SF_V]
        ] = callback
        if workflow:
            self.release(workflow=workflow)

    def set_callback(self, callback: Callable[..., Any]) -> None:
        self.callback = callback

    def release(self, workflow: WorkflowManager) -> None:
        for name, job in workflow.get_flow_pairs():
            self.tasks.append(JobExecutor(name=name, job=job))

    def check_needed(
        self, needs: Optional[List[str]], results: Dict[str, _EXEC_YT]
    ) -> Union[NoReturn, None]:
        if needs is None or all(name in results for name in needs):
            return None
        missing: List[str] = [name for name in needs if name not in results]
        raise ValueError(
            f"Not all needed tasks are completed. Missing: {missing}. "
            f"Available results: {list(results.keys())}"
        )

    def run(self) -> Generator[_EXEC_YT, _EXEC_ST, List[_CB_SF_V]]:
        try:
            results: Dict[str, _EXEC_YT] = {}
            for task in self.tasks:
                self.check_needed(needs=task.job["needs"], results=results)

                result: _EXEC_YT = task.execute()
                results[task.name] = result
                yield result

            return [self.callback(result) for result in results.values()]
        except Exception as e:
            raise RuntimeError(f"Error during execution: {e}") from e
