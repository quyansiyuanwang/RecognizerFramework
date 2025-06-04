from typing import Any

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("OCR")
class OCRExecutor(Executor):

    def __init__(self, job: Job) -> None:
        self.job: Job = job

    def execute(self, *args: Any, **kwargs: Any) -> Any:
        # Simulate OCR processing
        return f"Processed OCR: {self.job['description']}"
