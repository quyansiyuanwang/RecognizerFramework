from typing import Optional

from ....Typehints import Job
from ..base import IgnorableError


class MouseMoveError(IgnorableError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(message="Mouse move error occurred: " + message, job=job)
        self.job: Optional[Job] = job
        self.message: str = message


class MouseMovePositionError(MouseMoveError):
    def __init__(self, message: str, job: Optional[Job] = None):
        super().__init__(
            message="Mouse move position error occurred: " + message, job=job
        )
        self.job: Optional[Job] = job
        self.message: str = message
