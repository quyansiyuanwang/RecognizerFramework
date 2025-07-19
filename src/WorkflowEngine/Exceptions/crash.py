from typing import Optional

from ...Structure import Job
from .base import CrashException


class WorkflowError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(f"Workflow error in job '{job}': {message}", job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class WorkflowBeginError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__("Workflow begin error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class JobTypeError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__("Job type error: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class JobNotFoundError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(f"Job not found: {message}", job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class OverloadError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Overload error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class RecursiveError(OverloadError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(
            message="Recursive overload error occurred: " + message, job=job
        )
        self.job: Optional[Job] = job
        self.message: str = message


class TemplateError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Template error occurred: " + message, job=job)
        self.job: Optional[Job] = job


class NeededError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Needed error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class MissingRequiredError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Missing required error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class ActionTypeError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(
            message="System action type error occurred: " + message, job=job
        )
        self.job: Optional[Job] = job
        self.message: str = message


class LogLevelError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Log level error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class DebugError(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Debug error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


from .execs.roi_crash import *
from .execs.system_crash import *
