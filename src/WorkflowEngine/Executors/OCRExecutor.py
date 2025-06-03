from typing import Any

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("OCR")
class OCRExecutor(Executor):
    def execute(self, job: Job) -> Any:
        # Simulate OCR processing
        return f"Processed OCR: {job.description}"
