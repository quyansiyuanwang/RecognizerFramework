from typing import Any

from src.Structure import Action, Delay
from src.Typehints import GlobalsDict

from ..Controller import InputController, SystemController
from ..exceptions import ActionError
from ..executor import Executor, Job, JobExecutor


@JobExecutor.register("Input")
class InputExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def execute_TestInput(self, action: Action, delay: Delay) -> str:
        input_text = action.get("text", "")
        cur_delay = delay.get("cur", 0)

        InputController.typewrite(
            input_text, duration=cur_delay, debug=self.globals.get("debug", False)
        )
        return f"Typed input: {input_text}"

    def execute_MouseInput(self, action: Action, delay: Delay) -> str:
        x = action.get("x", 0)
        y = action.get("y", 0)
        cur_delay = delay.get("cur", 0)

        InputController.click(
            x, y, delay_ms=cur_delay, debug=self.globals.get("debug", False)
        )
        return f"Clicked at ({x}, {y}) with delay {cur_delay} ms"

    def execute_KeyboardInput(self, action: Action, delay: Delay) -> str:
        input_text = action.get("text", "")
        cur_delay = delay.get("cur", 0)
        keys = action.get("keys", None)
        if keys:
            input_text = keys

        InputController.keyboard_press_and_release(
            input_text, delay_ms=cur_delay, debug=self.globals.get("debug", False)
        )
        return f"Keyboard input: {input_text} with delay {cur_delay} ms"

    def execute(self, *args: Any, **kwargs: Any) -> str:
        delay: Delay = self.job.get("delay", {})
        pre_delay: int = delay.get("pre", 0)
        post_delay: int = delay.get("post", 0)

        SystemController.sleep(pre_delay, debug=self.globals.get("debug", False))

        action: Action = self.job.get("action", None)
        if not action:
            raise ActionError(self.job, "No action found in the job to execute.")

        res: str = "Unknown action type"
        try:
            if action.get("type") == "TextInput":
                res = self.execute_TestInput(action, delay)
            elif action.get("type") == "MouseInput":
                res = self.execute_MouseInput(action, delay)
            elif action.get("type") == "KeyboardInput":
                res = self.execute_KeyboardInput(action, delay)
        except Exception as e:
            raise e
        finally:
            SystemController.sleep(post_delay, debug=self.globals.get("debug", False))

        return res
