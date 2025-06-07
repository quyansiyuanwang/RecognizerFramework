from datetime import datetime
from enum import IntFlag
from typing import Dict, Iterable, List, Optional

from src.Typehints import LogConfigDict

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
    DEFAULT_LOG_CONFIG = LogConfigDict(
        level=LogLevel.INFO,
        file=None,
        format="%(levelname)s - %(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S.%f",
        clear=False,
    )
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
    def log(
        message: str,
        level: Iterable[LogLevel],
        log_config: Optional[LogConfigDict] = None,
    ) -> None:
        if log_config is None:
            log_config = Logger.DEFAULT_LOG_CONFIG
        levels = list(level)
        if not levels:
            color = Color.RESET
        else:
            highest_level = max(levels, key=lambda l: l.value)
            color = Logger.COLOR_MAP.get(highest_level, Color.RESET)

        msg_type = "][".join(Logger.ABBREVIATIONS.get(l, "UNK") for l in levels)
        date_formatted = datetime.now().strftime(
            log_config.get("datefmt", "%Y-%m-%d %H:%M:%S.%f")
        )
        params = {
            "asctime": date_formatted,
            "levelname": f"[{msg_type}]",
            "message": message,
        }
        final = (
            log_config.get("format", "%(levelname)s - %(asctime)s - %(message)s")
            % params
        )
        file = log_config.get("file")
        if file is not None:
            with open(file, "a", encoding="utf-8") as f:
                f.write(final + "\n")
        print(f"{color}{final}{Color.RESET}")

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


class LogManager:
    def __init__(
        self,
        debug: bool = False,
        level: LogLevel = LogLevel.INFO,
    ):
        self.debug: bool = debug
        self.level: LogLevel = level
        self.cleared: bool = False

    def log(
        self,
        msg: str,
        levels: Iterable[LogLevel],
        log_config: Optional[LogConfigDict] = None,
    ):
        if log_config is None:
            log_config = Logger.DEFAULT_LOG_CONFIG

        if log_config.get("clear", False) and not self.cleared:
            # 清空日志文件
            file = log_config.get("file")
            if file:
                with open(file, "w", encoding="utf-8") as f:
                    f.write("")
            self.cleared = True

        # 支持 debug 控制和日志级别过滤
        if self.debug or LogLevel.DEBUG in levels:
            Logger.log(
                message=msg,
                level=levels,
                log_config=log_config,
            )
        elif any(l >= self.level for l in levels):
            Logger.log(
                message=msg,
                level=levels,
                log_config=log_config,
            )

    def set_debug(self, debug: bool):
        self.debug = debug

    def set_level(self, level: LogLevel):
        self.level = level


global_log_manager = LogManager()
