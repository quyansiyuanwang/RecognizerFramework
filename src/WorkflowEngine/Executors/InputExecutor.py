from typing import Any

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("Input")
class InputExecutor(Executor):
    def execute(self, job: Job) -> Any:
        # Simulate input processing
        return f"Processed input: {job.description}"
