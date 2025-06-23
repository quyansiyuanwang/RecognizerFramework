from typing import Any, Dict, Final, Literal

from src.Structure import Delay, Input, Keyboard, Mouse, Text
from src.Typehints import GlobalsDict
from src.WorkflowEngine.Exceptions.crash import ActionTypeError

from ..Controller import InputController, SystemController
from ..Exceptions.crash import MissingRequiredError
from ..Exceptions.ignorable import MouseMoveError, MouseMovePositionError
from ..executor import Executor, Job, JobExecutor

BUTTON_MAP: Final[
    Dict[Literal["LClick", "RClick", "MClick"], Literal["LEFT", "RIGHT", "MIDDLE"]]
] = {
    "LClick": "LEFT",
    "RClick": "RIGHT",
    "MClick": "MIDDLE",
}


@JobExecutor.register("Input")
class InputExecutor(Executor):
    def __init__(self, job: Job, globals: GlobalsDict) -> None:
        self.job: Job = job
        self.globals: GlobalsDict = globals

    def execute_TextInput(self, text: Text) -> str:
        input_text = text.get("text", "")
        duration = text.get("duration", 0)

        InputController.typewrite(
            input_text, duration=duration, debug=self.globals.get("debug", False)
        )
        return f"Typed input: {input_text} with duration {duration} ms"

    def __dissolve_click(self, mouse: Mouse) -> str:
        x = mouse.get("x", None)
        y = mouse.get("y", None)
        duration = mouse.get("duration", 0)
        input_type = mouse.get("type", "LClick")
        button_type: Literal["LEFT", "RIGHT", "MIDDLE"] = BUTTON_MAP.get(
            input_type, "LEFT"
        )

        InputController.click(
            x,
            y,
            delay_ms=duration,
            debug=self.globals.get("debug", False),
            click_type=button_type,
        )
        return f"{input_type} clicked at ({x}, {y}) with duration {duration} ms"

    def __dissolve_move(self, mouse: Mouse) -> str:
        if not any(mouse.get(key, None) for key in ("x", "y")):
            raise MouseMovePositionError("Missing required any of keys: x, y", self.job)

        x = mouse.get("x", 0)
        y = mouse.get("y", 0)
        move_type = mouse.get("type", "Move")
        if move_type == "Move":
            InputController.move(x, y, debug=self.globals.get("debug", False))
        elif move_type == "MoveTo":
            InputController.move_to(x, y, debug=self.globals.get("debug", False))
        else:
            raise MouseMoveError(f"Unsupported mouse move type: {move_type}", self.job)
        return f"Mouse moved to ({x}, {y})"

    def execute_MouseInput(self, mouse: Mouse) -> str:
        if mouse.get("type") in {"Move", "MoveTo"}:
            return self.__dissolve_move(mouse)
        elif mouse.get("type") in {"LClick", "RClick", "MClick"}:
            return self.__dissolve_click(mouse)
        else:
            raise ActionTypeError(
                f"Unsupported mouse action type: {mouse.get('type')}", self.job
            )

    def execute_KeyboardInput(self, keyboard: Keyboard) -> str:
        input_text = keyboard.get("text", "")
        duration = keyboard.get("duration", 0)
        sep_time = keyboard.get("sep_time", 0)
        keys = keyboard.get("keys", None)
        if keys:
            input_text = keys

        InputController.keyboard_press_and_release(
            input_text,
            duration=duration,
            sep_time=sep_time,
            debug=self.globals.get("debug", False),
        )
        return f"Keyboard input: {input_text} with duration {duration} ms"

    def execute(self, *args: Any, **kwargs: Any) -> str:
        delay: Delay = self.job.get("delay", {})
        pre_delay: int = delay.get("pre", 0)
        post_delay: int = delay.get("post", 0)

        SystemController.sleep(
            pre_delay,
            debug=self.globals.get("debug", False),
            prefix="InputExecutorPreDelay",
        )

        inp: Input = self.job.get("input", None)
        if not inp:
            raise MissingRequiredError(
                "No input found in the job to execute.", self.job
            )

        res: str = "Unknown input type"
        try:
            if inp.get("type") == "Text":
                res = self.execute_TextInput(inp.get("text", ""))
            elif inp.get("type") == "Mouse":
                res = self.execute_MouseInput(inp.get("mouse", {}))
            elif inp.get("type") == "Keyboard":
                res = self.execute_KeyboardInput(inp.get("keyboard", {}))
        except Exception as e:
            raise e
        finally:
            SystemController.sleep(
                post_delay,
                debug=self.globals.get("debug", False),
                prefix="InputExecutorPostDelay",
            )

        return res
