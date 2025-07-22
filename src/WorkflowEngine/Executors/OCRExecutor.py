from typing import Any, Dict

from ...Typehints import Globals, TaskReturnsDict
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("OCR")
class OCRExecutor(Executor):

    def __init__(self, job: Job, globals: Globals) -> None:
        self.job: Job = job
        self.globals: Globals = globals
        self.use_vars: Dict[str, Any] = {}

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[str]:
        self.use_vars.update(kwargs)
        # Simulate OCR processing
        raise NotImplementedError("OCR processing is not implemented yet.")
        return f"Processed OCR: {self.job['description']}"
