from typing import Any, Dict, List, Optional, cast

from ...Models.globals import Globals
from ...Models.system import LogLevelLiteral, System, System_Command, System_Log
from ...Typehints.structure import TaskReturnsDict
from ..Controller import Logger, LogLevel, SystemController
from ..Exceptions.crash import (
    ActionTypeError,
    CommandCrash,
    LogLevelError,
    MissingRequiredError,
)
from ..executor import Executor, Job, JobExecutor
from ..Util.executor_works import update


@JobExecutor.register("System")
class SystemExecutor(Executor):
    def __init__(self, job: Job, globals: Globals) -> None:
        self.job: Job = job
        self.globals: Globals = globals
        self.use_vars: Dict[str, Any] = {}

    def execute_Command(self, command_pkg: System_Command) -> TaskReturnsDict[str]:
        update(command_pkg, self.use_vars)
        command = command_pkg.command
        args = command_pkg.args
        env = command_pkg.env
        cwd = command_pkg.cwd
        shell = command_pkg.shell
        wait = command_pkg.wait
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
                debug=self.globals.debug,
            )
            return TaskReturnsDict(
                returns=cast(Dict[str, str], command_pkg.returns),
                variables=var_s,
                result=f"Executed command: {full}",
            )
        except Exception as e:
            if command_pkg.ignore:
                return TaskReturnsDict(
                    returns=cast(Dict[str, str], command_pkg.returns),
                    variables=var_s,
                    result=f"Failed to execute command: {full}, but ignored.",
                )
            raise CommandCrash(
                f"Failed to execute command: {full}, error: {e}", self.job
            )

    def execute_Paste(self, system: System) -> TaskReturnsDict[str]:
        update(system, self.use_vars)
        content = SystemController.paste()
        return TaskReturnsDict(
            returns=cast(Dict[str, str], system.returns),
            variables={"type": system.type, "content": content},
            result=f"Executed paste: {content}",
        )

    def execute_Delay(self, system: System) -> TaskReturnsDict[str]:
        update(system, self.use_vars)
        duration: int = system.duration
        SystemController.sleep(
            duration,
            debug=self.globals.debug,
            prefix="SystemExecutorDelay",
        )
        return TaskReturnsDict(
            returns=cast(Dict[str, str], system.returns),
            variables={"type": system.type, "duration": duration},
            result=f"Executed delay: {duration} ms",
        )

    def execute_Log(self, log_dict: System_Log) -> TaskReturnsDict[str]:
        update(log_dict, self.use_vars)
        message: str = log_dict.message
        levels: List[LogLevelLiteral] = log_dict.levels
        if not LogLevel.is_all_available(levels=levels):
            raise LogLevelError(f"Invalid log levels: {levels}", self.job)
        Logger.log(message, level=map(LogLevel.from_str, levels))
        return TaskReturnsDict(
            returns=cast(Dict[str, str], log_dict.returns),
            variables={
                "message": message,
                "levels": levels,
            },
            result=f"Logged message: {message} at levels: {levels}",
        )

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[str]:
        self.use_vars.update(kwargs)
        system: Optional[System] = self.job.system
        if system is None:
            raise MissingRequiredError(
                "No system action found in the job to execute.", self.job
            )

        if system.type == "Delay" and system:
            return self.execute_Delay(system)
        elif system.type == "Log" and system.log:
            return self.execute_Log(system.log)
        elif system.type == "Paste" and system:
            return self.execute_Paste(system)
        elif system.type == "Command" and system.command:
            return self.execute_Command(system.command)
        raise ActionTypeError(
            f"Unsupported type({system.type}) or missing field({system.type.lower()})",
            self.job,
        )
