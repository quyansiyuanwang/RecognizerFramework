from typing import Optional

from ....Models.main import Job
from ..base import IgnorableError


class ROIError(IgnorableError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="ROI error occurred: " + message, job=job)
        self.job: Optional[Job] = job


class MatchingError(ROIError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Matching error occurred: " + message, job=job)
        self.job: Optional[Job] = job
