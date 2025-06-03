import importlib
import os
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union

from ..Structure import Job
from .manager import WorkflowManager


class Executor(ABC):
    @abstractmethod
    def execute(self, job: Job) -> Any:
        pass


class JobExecutor:
    executors: Dict[str, Type[Executor]] = {}

    def __init__(self, job: Job):
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
    def register(cls, name: str):
        def decorator(executor: Union[Type[Executor], Any]):
            if not issubclass(executor, Executor):
                raise TypeError(f"{name} must be a subclass of Executor")
            cls.executors[name] = executor
            return executor

        return decorator

    def __call__(self):
        if self.job["type"] in self.executors:
            executor_class = self.executors[self.job["type"]]
            executor_instance = executor_class()
            return executor_instance.execute(self.job)
        else:
            assert False, f"Unknown job type: {self.job['type']}"


class ExecutorManager:
    def __init__(self, workflow: Optional[WorkflowManager] = None):
        self.tasks: List[JobExecutor] = []
        if workflow:
            self.release(workflow)

    def release(self, workflow: WorkflowManager):
        for job in workflow.jobs():
            self.tasks.append(JobExecutor(job))

    def run(self) -> List[str]:
        results: List[str] = []
        for task in self.tasks:
            result = task()
            results.append(result)
        return results


JobExecutor.import_trigger("src.WorkflowEngine.Executors")
