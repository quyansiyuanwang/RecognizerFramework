from typing import Optional

from ...Structure import Job
from .base import IgnorableError
from .execs.input import *
from .execs.roi import *
from .execs.system import *


class AfterJobRunError(IgnorableError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="After job run error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message
