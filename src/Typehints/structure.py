from typing import Any, Dict, Generic, TypedDict, TypeVar

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


_TaskReturnVar = TypeVar("_TaskReturnVar")


class TaskReturnsDict(TypedDict, Generic[_TaskReturnVar]):
    result: _TaskReturnVar
    returns: Dict[str, str]
    variables: Dict[str, Any]
