from enum import IntFlag
from typing import Dict, Iterable, List

from ..Util import Color


class LogLevel(IntFlag):
    LOG = 1
    DEBUG = 2
    INFO = 4
    WARNING = 8
    ERROR = 16

    @classmethod
    def from_value(cls, value: int) -> List["LogLevel"]:
        members = [member for member in cls if member.value & value]
        return members


class Logger:
    COLOR_MAP: Dict[LogLevel, str] = {
        LogLevel.LOG: Color.WHITE,
        LogLevel.DEBUG: Color.BLUE,
        LogLevel.ERROR: Color.RED,
        LogLevel.WARNING: Color.YELLOW,
        LogLevel.INFO: Color.GREEN,
    }
    ABBREVIATIONS: Dict[LogLevel, str] = {
        LogLevel.LOG: "LOG",
        LogLevel.DEBUG: "DBG",
        LogLevel.ERROR: "ERR",
        LogLevel.WARNING: "WRN",
        LogLevel.INFO: "INF",
    }

    @staticmethod
    def log(message: str, level: Iterable[LogLevel]) -> None:
        levels = list(level)
        if not levels:
            color = Color.RESET
        else:
            highest_level = max(levels, key=lambda l: l.value)
            color = Logger.COLOR_MAP.get(highest_level, Color.RESET)

        msg_type = "|".join(Logger.ABBREVIATIONS.get(l, "UNK") for l in levels)
        formatted_message = f"[{msg_type}] {message}"
        print(f"{color}{formatted_message}{Color.RESET}")

    @staticmethod
    def error(message: str) -> None:
        Logger.log(message, [LogLevel.ERROR])

    @staticmethod
    def warning(message: str) -> None:
        Logger.log(message, [LogLevel.WARNING])

    @staticmethod
    def info(message: str) -> None:
        Logger.log(message, [LogLevel.INFO])

    @staticmethod
    def debug(message: str) -> None:
        Logger.log(message, [LogLevel.DEBUG])
