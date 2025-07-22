from typing import Optional

from ...Typehints import Job


class ExecutionError(Exception):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(f"Execution error in job '{job}': \n{message}")
        self.message: str = message


class IgnorableError(ExecutionError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(f"Ignorable error in job '{job}': {message}", job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class CriticalException(ExecutionError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__("Crash exception occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class CrashException(ExecutionError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__("Crash exception occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message
