from typing import TypedDict


class TaskAttemptDict(TypedDict):
    success: int
    failure: int
