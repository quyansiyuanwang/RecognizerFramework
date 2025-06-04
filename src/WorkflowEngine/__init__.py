from typing import List

from .executor import Executor, ExecutorManager, JobExecutor
from .manager import WorkflowManager

# init built-in Executors
JobExecutor.import_trigger("src.WorkflowEngine.Executors")

__all__: List[str] = [
    # executor
    "ExecutorManager",
    "JobExecutor",
    "Executor",
    # manager
    "WorkflowManager",
]
