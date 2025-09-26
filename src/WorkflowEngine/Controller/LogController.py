from datetime import datetime
from enum import IntFlag
from typing import Dict, Iterable, List, Literal, Optional, Union

from ...Models.globals import Globals, LogConfig
from ...Models.system import LogLevelLiteral
from ...Util.path_util import get_current_dir, is_absolute_path
from ..Util.style import Color


class LogLevel(IntFlag):
    LOG = 1
    DEBUG = 2
    INFO = 4
    WARNING = 8
    ERROR = 16
    CRITICAL = 32

    @staticmethod
    def is_all_available(
        levels: Union[List[LogLevelLiteral], List["LogLevel"]],
    ) -> bool:
        if not levels:
            return False
        if all(isinstance(l, str) for l in levels) and all(
            l in LogLevel.get_available_strs() for l in levels
        ):
            return True
        if all(isinstance(l, LogLevel) for l in levels):
            return True

        return False

    @staticmethod
    def get_available_strs() -> List[str]:
        return ["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def from_value(cls, value: int) -> List["LogLevel"]:
        members = [member for member in cls if member.value & value]
        return members

    @classmethod
    def from_str(
        cls,
        value: Union[
            str,
            Literal["LOG", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        ],
    ) -> "LogLevel":
        value = value.upper()
        if value == "LOG":
            return cls.LOG
        elif value == "DEBUG":
            return cls.DEBUG
        elif value == "INFO":
            return cls.INFO
        elif value == "WARNING":
            return cls.WARNING
        elif value == "ERROR":
            return cls.ERROR
        elif value == "CRITICAL":
            return cls.CRITICAL
        else:
            raise ValueError(f"Unknown log level: {value}")


class Logger:
    DEFAULT_LOG_CONFIG = LogConfig(
        level="LOG",
        file="",
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
        LogLevel.CRITICAL: Color.MAGENTA,
    }
    ABBREVIATIONS: Dict[LogLevel, str] = {
        LogLevel.LOG: "LOG",
        LogLevel.DEBUG: "DBG",
        LogLevel.ERROR: "ERR",
        LogLevel.WARNING: "WRN",
        LogLevel.INFO: "INF",
        LogLevel.CRITICAL: "CRT",
    }

    @staticmethod
    def log(
        message: str,
        level: Iterable[LogLevel],
        log_config: Optional[LogConfig] = None,
        colorful: bool = True,
    ) -> None:
        if log_config is None:
            log_config = Logger.DEFAULT_LOG_CONFIG
        levels = list(level)
        if colorful and levels:
            highest_level = max(levels, key=lambda l: l.value)
            color = Logger.COLOR_MAP.get(highest_level, Color.RESET)
        else:
            color = Color.RESET if colorful else ""

        tail = "" if not colorful else Color.RESET
        msg_type = "][".join(Logger.ABBREVIATIONS.get(l, "UNK") for l in levels)
        date_formatted = datetime.now().strftime(log_config.datefmt)
        params = {
            "asctime": date_formatted,
            "levelname": f"[{msg_type}]",
            "message": message,
        }
        final = log_config.format % params
        file = log_config.file
        if not is_absolute_path(file) and file:
            file = get_current_dir(file)

        if file:
            with open(file, "a", encoding="utf-8") as f:
                f.write(final + "\n")
        print(f"{color}{final}{tail}")

    @staticmethod
    def error(message: str, colorful: bool = True) -> None:
        Logger.log(message, [LogLevel.ERROR], colorful=colorful)

    @staticmethod
    def warning(message: str, colorful: bool = True) -> None:
        Logger.log(message, [LogLevel.WARNING], colorful=colorful)

    @staticmethod
    def info(message: str, colorful: bool = True) -> None:
        Logger.log(message, [LogLevel.INFO], colorful=colorful)

    @staticmethod
    def debug(message: str, colorful: bool = True) -> None:
        Logger.log(message, [LogLevel.DEBUG], colorful=colorful)


class LogManager:

    def __init__(
        self,
        debug: bool = False,
        level: LogLevel = LogLevel.LOG,
    ):
        self.debug: bool = debug
        self.level: LogLevel = level
        self.colorful: bool = True
        self.__cleared: bool = False
        self.globals_: Globals = Globals()

    def log(
        self,
        msg: str,
        levels: Iterable[LogLevel],
        debug: bool = False,
        log_config: Optional[LogConfig] = None,
        colorful: Optional[bool] = None,
    ):
        if log_config is None:
            log_config = self.globals_.logConfig

        if not self.__cleared and log_config.clear:
            # 清空日志文件
            file = log_config.file
            if not is_absolute_path(file) and file:
                file = get_current_dir(file)

            if file:
                with open(file, "w", encoding="utf-8") as f:
                    f.write("")
            self.__cleared = True

        # 支持 debug 控制和日志级别过滤
        if not debug and LogLevel.DEBUG in levels:
            return

        if any(l >= self.level for l in levels):
            Logger.log(
                message=msg,
                level=levels,
                log_config=log_config,
                colorful=colorful or self.colorful,
            )

    def set_debug(self, debug: bool):
        self.debug = debug

    def set_globals(self, globals_: Globals):
        self.globals_ = globals_

    def set_level(self, level: LogLevel):
        self.level = level

    def set_level_str(
        self,
        level: Union[
            Literal[
                "LOG",
                "DEBUG",
                "INFO",
                "WARNING",
                "ERROR",
                "CRITICAL",
            ],
            str,
        ],
    ):
        self.set_level(LogLevel.from_str(level))


global_log_manager = LogManager()
