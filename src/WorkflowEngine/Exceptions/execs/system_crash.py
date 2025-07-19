from typing import Optional

from ....Structure import Job
from ..base import CrashException


class CommandCrash(CrashException):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(
            message="Command execution error occurred: " + message, job=job
        )
        self.job: Optional[Job] = job
        self.message: str = message
