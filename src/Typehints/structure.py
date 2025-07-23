from typing import Any, Dict, Generic, TypedDict, TypeVar


# Workflow Engine Type Hints
class TaskAttemptDict(TypedDict):
    success: int
    failure: int


_TaskReturnVar = TypeVar("_TaskReturnVar")


class TaskReturnsDict(TypedDict, Generic[_TaskReturnVar]):
    result: _TaskReturnVar
    returns: Dict[str, str]
    variables: Dict[str, Any]
