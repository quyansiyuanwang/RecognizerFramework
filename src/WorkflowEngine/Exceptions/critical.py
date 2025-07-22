from typing import Optional

from ...Typehints import Job
from .base import CriticalException


class RetryError(CriticalException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Retry error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message
