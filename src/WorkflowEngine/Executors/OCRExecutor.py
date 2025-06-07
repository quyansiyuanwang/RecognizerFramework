from typing import Any

from src.Typehints import GlobalsDict

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("OCR")
class OCRExecutor(Executor):

    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def execute(self, *args: Any, **kwargs: Any) -> str:
        # Simulate OCR processing
        raise NotImplementedError("OCR processing is not implemented yet.")
        return f"Processed OCR: {self.job['description']}"
