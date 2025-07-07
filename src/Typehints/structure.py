from typing import TypedDict

from PIL.Image import Image as PILImage


# Executor Type Hints
## ROIExecutor Type Hints
class WindowLocationDict(TypedDict):
    left: int
    top: int
    mat: PILImage


# Workflow Engine Type Hints
class TaskAttemptDict(TypedDict):
    success: int
    failure: int
