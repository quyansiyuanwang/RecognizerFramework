from typing import (
    Any,
    Dict,
    List,
    Literal,
    NotRequired,
    Optional,
    TypeAlias,
    TypedDict,
    Union,
)


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
    type: Literal[
        "LClick",
        "RClick",
        "DoubleClick",
        "TextInput",
        "KeyboardInput",
        "Delay",
        "Paste",
        "Typewrite",
        "Hotkey",
    ]
    position: NotRequired[PositionDict]
    duration: NotRequired[int]
    keys: NotRequired[List[str]]
    text: NotRequired[str]
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
    name: str  # NOTE: special field, job name
    # Required fields
    type: Literal["ROI", "OCR", "Input", "System"]
    action: ActionDict
    # Optional fields
    description: NotRequired[str]
    image: NotRequired[ImageDict]
    region: NotRequired[RegionDict]
    next: NotRequired[Union[str, NextDict]]
    delay: NotRequired[DelayDict]
    limits: NotRequired[LimitsDict]


class LogConfigDict(TypedDict):
    level: int
    file: NotRequired[Optional[str]]
    format: NotRequired[str]
    datefmt: NotRequired[str]
    clear: NotRequired[bool]


class IdentifiedGlobalsDict(TypedDict):
    debug: NotRequired[bool]
    colorful: NotRequired[bool]
    ignore: NotRequired[bool]
    logConfig: NotRequired[LogConfigDict]


GlobalsDict: TypeAlias = Union[IdentifiedGlobalsDict, Dict[str, Any]]


class WorkflowDict(TypedDict):
    begin: str
    globals: NotRequired[GlobalsDict]
    jobs: Dict[str, JobDict]
