from typing import Any, Dict, Final, Literal

from ...Structure import Keyboard, Mouse, Text
from ...Typehints import GlobalsDict
from ..Controller import InputController
from ..Exceptions.crash import ActionTypeError, MissingRequiredError
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
        message = text.get("message", "")
        duration = text.get("duration", 0)

        InputController.typewrite(
            message, duration=duration, debug=self.globals.get("debug", False)
        )
        return f"Typed input: {message} with duration {duration} ms"

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
        duration = keyboard.get("duration", 0)
        sep_time = keyboard.get("sep_time", 0)
        keys = keyboard.get("keys", None)

        InputController.keyboard_press_and_release(
            keys,
            duration=duration,
            sep_time=sep_time,
            debug=self.globals.get("debug", False),
        )
        return f"Keyboard input: {keys} with duration {duration} ms"

    def execute(self, *args: Any, **kwargs: Any) -> str:
        inp = self.job.get("input", None)
        if not inp:
            raise MissingRequiredError(
                "No input found in the job to execute.", self.job
            )

        if inp.get("type") == "Text":
            return self.execute_TextInput(inp.get("text", ""))
        elif inp.get("type") == "Mouse":
            return self.execute_MouseInput(inp.get("mouse", {}))
        elif inp.get("type") == "Keyboard":
            return self.execute_KeyboardInput(inp.get("keyboard", {}))
        else:
            raise ActionTypeError(
                f"Unsupported input type: {inp.get('type')}", self.job
            )
