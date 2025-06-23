from typing import Any, List

from src.Structure import Delay
from src.Typehints import GlobalsDict, LogDict, LogLevelLiteral
from src.WorkflowEngine.Exceptions.crash import ActionTypeError, LogLevelError

from ..Controller import Logger, LogLevel, SystemController
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
        delay: Delay = self.job.get("delay", {})
        pre_delay: int = delay.get("pre", 0)
        post_delay: int = delay.get("post", 0)
        SystemController.sleep(
            pre_delay,
            debug=self.globals.get("debug", False),
            prefix="SystemExecutorPreDelay",
        )
        action = self.job.get("system", None)
        try:
            if action.get("type") == "Delay":
                return self.execute_Delay(action)
            elif action.get("type") == "Log":
                return self.execute_Log(action.get("log", {}))
            raise ActionTypeError(f"Unsupported action: {action.get('type')}", self.job)
        except Exception as e:
            raise e
        finally:
            post_delay = self.job.get("delay", {}).get("post", 0)
            SystemController.sleep(
                post_delay,
                debug=self.globals.get("debug", False),
                prefix="SystemExecutorPostDelay",
                levels=[LogLevel.DEBUG],
            )
