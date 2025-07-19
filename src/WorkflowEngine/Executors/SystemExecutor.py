from typing import Any, List, Optional

from ...Structure import System
from ...Typehints import GlobalsDict, LogLevelLiteral
from ..Controller import Logger, LogLevel, SystemController
from ..Exceptions.crash import ActionTypeError, LogLevelError, MissingRequiredError
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("System")
class SystemExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def execute_Paste(self, system: System) -> str:
        content = SystemController.paste()
        return f"Executed paste: {content}"

    def execute_Delay(self, system: System) -> str:
        duration: int = system.get("duration", 0)
        SystemController.sleep(
            duration,
            debug=self.globals.get("debug", False),
            prefix="SystemExecutorDelay",
        )
        return f"Executed delay: {duration} ms"

    def execute_Log(self, system: System) -> str:
        log_dict = system.get("log", {})
        message: str = log_dict.get("message", "")
        levels: List[LogLevelLiteral] = log_dict.get("levels", ["LOG"])
        if not LogLevel.is_all_available(levels=levels):
            raise LogLevelError(f"Invalid log levels: {levels}", self.job)
        Logger.log(message, level=map(LogLevel.from_str, levels))
        return f"Logged message: {message} at levels: {levels}"

    def execute(self, *args: Any, **kwargs: Any) -> str:
        system: Optional[System] = self.job.get("system", None)
        if system is None:
            raise MissingRequiredError(
                "No system action found in the job to execute.", self.job
            )

        if system.get("type") == "Delay":
            return self.execute_Delay(system)
        elif system.get("type") == "Log":
            return self.execute_Log(system)
        elif system.get("type") == "Paste":
            return self.execute_Paste(system)
        raise ActionTypeError(f"Unsupported action: {system.get('type')}", self.job)
