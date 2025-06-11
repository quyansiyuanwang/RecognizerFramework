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


LogLevelLiteral = Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class ActionDict(TypedDict):
    type: Literal[
        "LClick",
        "RClick",
        "DoubleClick",
        "TextInput",
        "KeyboardInput",
        "Delay",
        "Paste",
        "Log",
    ]
    position: NotRequired[PositionDict]
    duration: NotRequired[int]
    keys: NotRequired[List[str]]
    text: NotRequired[str]
    message: NotRequired[str]
    levels: NotRequired[List[LogLevelLiteral]]
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
    type: Literal["ROI", "OCR", "Input", "System", "Overload"]
    action: ActionDict
    # Optional fields
    description: NotRequired[str]
    image: NotRequired[ImageDict]
    region: NotRequired[RegionDict]
    next: NotRequired[Union[str, NextDict]]
    delay: NotRequired[DelayDict]
    limits: NotRequired[LimitsDict]
    overload: NotRequired[str]


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
    logLevel: NotRequired[
        Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    ]
    logConfig: NotRequired[LogConfigDict]


GlobalsDict: TypeAlias = Union[IdentifiedGlobalsDict, Dict[str, Any]]


class WorkflowDict(TypedDict):
    begin: str
    globals: NotRequired[GlobalsDict]
    jobs: Dict[str, JobDict]
