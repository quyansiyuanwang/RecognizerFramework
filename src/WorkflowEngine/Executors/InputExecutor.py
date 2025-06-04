from typing import Any

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("Input")
class InputExecutor(Executor):
    def __init__(self, job: Job) -> None:
        self.job: Job = job

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        # Simulate input processing
        return f"Processed input: {self.job['description']}"
