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

from .input import InputDict
from .job_params import DelayDict, LimitsDict, NextDict, UseDict
from .roi import ROIDict
from .system import LogLevelLiteral, SystemDict


class JobDict(TypedDict):
    name: str  # NOTE: special field, job name
    # Required fields
    type: Literal["ROI", "OCR", "Input", "System", "Overload"]

    # Optional fields
    description: NotRequired[str]
    delay: NotRequired[DelayDict]
    limits: NotRequired[LimitsDict]
    needs: NotRequired[List[str]]
    next: NotRequired[Union[str, NextDict]]
    overload: NotRequired[str]
    use: NotRequired[UseDict]

    # Action fields
    roi: NotRequired[ROIDict]
    input: NotRequired[InputDict]
    system: NotRequired[SystemDict]


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
    logLevel: NotRequired[LogLevelLiteral]
    logConfig: NotRequired[LogConfigDict]


GlobalsDict: TypeAlias = Union[IdentifiedGlobalsDict, Dict[str, Any]]


class WorkflowDict(TypedDict):
    begin: str
    globals: NotRequired[GlobalsDict]
    jobs: Dict[str, JobDict]
