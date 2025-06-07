from typing import Any, Dict, NotRequired, TypedDict, Union


class ImageDict(TypedDict):
    path: str
    confidence: NotRequired[float]


class RegionDict(TypedDict):
    x: int
    y: int
    width: int
    height: int


class PositionDict(TypedDict):
    type: str  # "Absolute" | "Relative"
    x: NotRequired[int]
    y: NotRequired[int]


class ActionDict(TypedDict):
    type: str
    position: NotRequired[PositionDict]
    keys: NotRequired[list[str]]
    text: NotRequired[str]
    duration: NotRequired[int]
    use_keyboard: NotRequired[bool]


class DelayDict(TypedDict):
    pre: NotRequired[int]
    cur: NotRequired[int]
    post: NotRequired[int]


class NextDict(TypedDict):
    success: NotRequired[str]
    failure: NotRequired[str]


class LimitsDict(TypedDict):
    maxCount: NotRequired[int]
    maxFailure: NotRequired[int]
    maxSuccess: NotRequired[int]


class JobDict(TypedDict):
    type: str
    action: NotRequired[ActionDict]
    description: NotRequired[str]
    image: NotRequired[ImageDict]
    region: NotRequired[RegionDict]
    next: NotRequired[Union[str, NextDict]]
    delay: NotRequired[DelayDict]
    needs: NotRequired[list[str]]
    limits: NotRequired[LimitsDict]


class IdentifiedGlobalsDict(TypedDict):
    debug: NotRequired[bool]
    colorful: NotRequired[bool]
    ignore: NotRequired[bool]


GlobalsDict = Union[IdentifiedGlobalsDict, Dict[str, Any]]


class WorkflowDict(TypedDict):
    begin: str
    globals: NotRequired[GlobalsDict]
    jobs: Dict[str, JobDict]
