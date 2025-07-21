from typing import Any, Dict, List, Optional

from ...Structure import System, System_Command, System_Log
from ...Typehints import GlobalsDict, LogLevelLiteral, TaskReturnsDict
from ..Controller import Logger, LogLevel, SystemController
from ..Exceptions.crash import (
    ActionTypeError,
    CommandCrash,
    LogLevelError,
    MissingRequiredError,
)
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("System")
class SystemExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals
        self.use_vars: Dict[str, Any] = {}

    def execute_Command(self, command_pkg: System_Command) -> TaskReturnsDict[str]:
        command_pkg.update(self.use_vars)
        command = command_pkg.get("command", "")
        args = command_pkg.get("args", [])
        env = command_pkg.get("env", None)
        cwd = command_pkg.get("cwd", None)
        shell = command_pkg.get("shell", True)
        wait = command_pkg.get("wait", True)
        full = f"{command} {' '.join(args)}"
        var_s: Dict[str, Any] = {
            "command": command,
            "args": args,
            "env": env,
            "cwd": cwd,
            "shell": shell,
            "wait": wait,
            "full_command": full,
        }
        try:
            SystemController.run_command(
                command,
                args=args,
                env=env,
                cwd=cwd,
                shell=shell,
                wait=wait,
                debug=self.globals.get("debug", False),
            )
            return TaskReturnsDict(
                returns=command_pkg.get("returns", {}),
                variables=var_s,
                result=f"Executed command: {full}",
            )
        except Exception as e:
            if command_pkg.get("ignore", False):
                return TaskReturnsDict(
                    returns=command_pkg.get("returns", {}),
                    variables=var_s,
                    result=f"Failed to execute command: {full}, but ignored.",
                )
            raise CommandCrash(
                f"Failed to execute command: {full}, error: {e}", self.job
            )

    def execute_Paste(self, system: System) -> TaskReturnsDict[str]:
        system.update(self.use_vars)
        content = SystemController.paste()
        return TaskReturnsDict(
            returns=system.get("returns", {}),
            variables={"type": system.get("type"), "content": content},
            result=f"Executed paste: {content}",
        )

    def execute_Delay(self, system: System) -> TaskReturnsDict[str]:
        system.update(self.use_vars)
        duration: int = system.get("duration", 0)
        SystemController.sleep(
            duration,
            debug=self.globals.get("debug", False),
            prefix="SystemExecutorDelay",
        )
        return TaskReturnsDict(
            returns=system.get("returns", {}),
            variables={"type": system.get("type"), "duration": duration},
            result=f"Executed delay: {duration} ms",
        )

    def execute_Log(self, log_dict: System_Log) -> TaskReturnsDict[str]:
        log_dict.update(self.use_vars)
        message: str = log_dict.get("message", "")
        levels: List[LogLevelLiteral] = log_dict.get("levels", ["LOG"])
        if not LogLevel.is_all_available(levels=levels):
            raise LogLevelError(f"Invalid log levels: {levels}", self.job)
        Logger.log(message, level=map(LogLevel.from_str, levels))
        return TaskReturnsDict(
            returns=log_dict.get("returns", {}),
            variables={
                "message": message,
                "levels": levels,
            },
            result=f"Logged message: {message} at levels: {levels}",
        )

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[str]:
        self.use_vars.update(kwargs)
        system: Optional[System] = self.job.get("system", None)
        if system is None:
            raise MissingRequiredError(
                "No system action found in the job to execute.", self.job
            )

        if system.get("type") == "Delay":
            return self.execute_Delay(system)
        elif system.get("type") == "Log":
            return self.execute_Log(system.get("log", {}))
        elif system.get("type") == "Paste":
            return self.execute_Paste(system)
        elif system.get("type") == "Command":
            return self.execute_Command(system.get("command", {}))
        raise ActionTypeError(f"Unsupported action: {system.get('type')}", self.job)
