from typing import List, Literal, NotRequired, TypedDict

LogLevelLiteral = Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class LogDict(TypedDict):
    message: str
    levels: List[LogLevelLiteral]


class SystemDict(TypedDict):
    # Required fields
    type: Literal["Delay", "Log", "Paste"]

    # Optional fields
    duration: NotRequired[int]
    log: NotRequired[LogDict]
