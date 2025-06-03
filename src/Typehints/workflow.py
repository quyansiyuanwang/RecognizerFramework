from typing import Dict, Literal, NotRequired, TypedDict


class ImageDict(TypedDict):
    path: str
    confidence: float


class RegionDict(TypedDict):
    x: int
    y: int
    width: int
    height: int


class PositionDict(TypedDict):
    type: Literal["absolute", "relative"]
    x: NotRequired[int]
    y: NotRequired[int]


class ActionDict(TypedDict):
    type: Literal["LClick", "RClick", "DoubleClick", "TextInput"]
    position: NotRequired[PositionDict]


class DelayDict(TypedDict):
    pre: NotRequired[int]
    cur: NotRequired[int]
    post: NotRequired[int]


class JobDict(TypedDict):
    # Required fields
    type: Literal["image", "ocr", "text_input"]
    action: ActionDict
    # Optional fields
    description: NotRequired[str]
    image: NotRequired[ImageDict]
    region: NotRequired[RegionDict]
    next: NotRequired[str]
    delay: NotRequired[DelayDict]


class WorkflowDict(TypedDict):
    begin: str
    jobs: Dict[str, JobDict]
