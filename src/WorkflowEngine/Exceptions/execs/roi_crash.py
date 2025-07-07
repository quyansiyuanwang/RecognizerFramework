from typing import Optional

from ....Structure import Job
from ..base import CrashException
from .roi import ROIError


class RegionError(ROIError, CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Region error occurred: " + message, job=job)
        self.job: Optional[Job] = job


class MultipleMatchedError(ROIError, CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(
            message="Multiple matched crash error occurred: " + message, job=job
        )
        self.job: Optional[Job] = job


class WindowNotFoundError(ROIError, CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Window not found error occurred: " + message, job=job)
        self.job: Optional[Job] = job


class IllegalWindowAreaError(ROIError, CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(
            message="Illegal window area error occurred: " + message, job=job
        )
        self.job: Optional[Job] = job
