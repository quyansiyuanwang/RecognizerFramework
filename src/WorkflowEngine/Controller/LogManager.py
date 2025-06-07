from typing import List

from .LogController import Logger, LogLevel


class LogManager:
    def __init__(self, debug: bool = False, level: LogLevel = LogLevel.INFO):
        self.debug = debug
        self.level = level

    def log(self, msg: str, levels: List[LogLevel]):
        # 支持 debug 控制和日志级别过滤
        if self.debug or LogLevel.DEBUG in levels:
            Logger.log(msg, levels)
        elif any(l >= self.level for l in levels):
            Logger.log(msg, levels)

    def set_debug(self, debug: bool):
        self.debug = debug

    def set_level(self, level: LogLevel):
        self.level = level
