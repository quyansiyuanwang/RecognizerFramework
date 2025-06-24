from typing import Any, List

from ...Structure import Delay
from ...Typehints import GlobalsDict, LogDict, LogLevelLiteral
from ..Controller import Logger, LogLevel, SystemController
from ..Exceptions.crash import ActionTypeError, LogLevelError, MissingRequiredError
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("System")
class SystemExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def execute_Delay(self, delay: Delay) -> str:
        duration: int = delay.get("duration", 0)
        SystemController.sleep(
            duration,
            debug=self.globals.get("debug", False),
            prefix="SystemExecutorDelay",
        )
        return f"Executed delay: {duration} ms"

    def execute_Log(self, action: LogDict) -> str:
        message: str = action.get("message", "")
        levels: List[LogLevelLiteral] = action.get("levels", ["LOG"])
        if not LogLevel.is_all_available(levels=levels):
            raise LogLevelError(f"Invalid log levels: {levels}", self.job)
        Logger.log(message, level=map(LogLevel.from_str, levels))
        return f"Logged message: {message} at levels: {levels}"

    def execute(self, *args: Any, **kwargs: Any) -> str:
        action = self.job.get("system", None)
        if action is None:
            raise MissingRequiredError(
                "No system action found in the job to execute.", self.job
            )
        if action.get("type") == "Delay":
            return self.execute_Delay(action)
        elif action.get("type") == "Log":
            return self.execute_Log(action.get("log", {}))
        raise ActionTypeError(f"Unsupported action: {action.get('type')}", self.job)
