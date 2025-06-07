from typing import Any

from src.Structure.delay import Delay
from src.Typehints import ActionDict, GlobalsDict
from src.WorkflowEngine.Controller import SystemController
from src.WorkflowEngine.exceptions import ArgumentError, JobTypeError

from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("System")
class SystemExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def execute_Delay(self, action: ActionDict) -> str:
        duration = action.get("duration", 0)
        SystemController.sleep(duration, debug=self.globals.get("debug", False))
        return f"Executed delay: {duration} ms"

    def execute(self, *args: Any, **kwargs: Any) -> str:
        delay: Delay = self.job.get("delay", {})
        pre_delay: int = delay.get("pre", 0)
        post_delay: int = delay.get("post", 0)
        action = self.job.get("action", None)
        SystemController.sleep(pre_delay, debug=self.globals.get("debug", False))
        if not action:
            raise ArgumentError(self.job, "No action found in the job to execute.")
        try:
            if action.get("type") == "Delay":
                return self.execute_Delay(action)

            raise JobTypeError(self.job, f"Unsupported action: {action}")
        except Exception as e:
            raise e
        finally:
            post_delay = self.job.get("delay", {}).get("post", 0)
            SystemController.sleep(post_delay, debug=self.globals.get("debug", False))
            return f"Executed job: {self.job['name']}"
