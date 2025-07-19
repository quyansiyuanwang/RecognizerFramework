from typing import Any, Final, Optional, Set

from ...Structure import Keyboard, Mouse, Text
from ...Typehints import GlobalsDict
from ..Controller import InputController
from ..Exceptions.crash import ActionTypeError, MissingRequiredError
from ..Exceptions.ignorable import MouseMovePositionError
from ..executor import Executor, Job, JobExecutor

AVAILABLE_MOUSE_BUTTONS: Final[Set[str]] = {
    "LEFT",
    "RIGHT",
    "MIDDLE",
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

    def __dissolve_event(self, mouse: Mouse):
        button = mouse.get("button", "LEFT")
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )
        mt = mouse.get("type")
        InputController.mouse_event(
            mt,
            button=button.lower(),
            debug=self.globals.get("debug", False),
        )
        return f"{button} mouse button {mt.lower()}ed"

    def __dissolve_move(self, mouse: Mouse) -> str:
        if not any(mouse.get(key, None) for key in ("x", "y")):
            raise MouseMovePositionError("Missing required any of keys: x, y", self.job)

        x: int = mouse.get("x", 0)
        y: int = mouse.get("y", 0)
        duration = mouse.get("duration", 0)
        relative = mouse.get("relative", False)
        button = mouse.get("button", "LEFT")
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )
        if relative:
            cur_pos = InputController.get_mouse_position()
            x += cur_pos[0]
            y += cur_pos[1]

        InputController.mouse_move_to(
            x,
            y,
            duration=duration,
            debug=self.globals.get("debug", False),
            ignore=self.globals.get("ignore", False),
        )

        return f"Mouse moved to ({x}, {y}) with duration {duration} ms"

    def __dissolve_drag(self, mouse: Mouse) -> str:
        if not any(mouse.get(key, None) for key in ("x", "y")):
            raise MouseMovePositionError("Missing required any of keys: x, y", self.job)

        x: int = mouse.get("x", 0)
        y: int = mouse.get("y", 0)
        duration = mouse.get("duration", 0)
        relative = mouse.get("relative", False)
        button = mouse.get("button", "LEFT")
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )
        cur_pos = InputController.get_mouse_position()
        if relative:
            x += cur_pos[0]
            y += cur_pos[1]

        InputController.mouse_drag_to(
            button=button.lower(),
            x=x,
            y=y,
            duration=duration,
            debug=self.globals.get("debug", False),
            ignore=self.globals.get("ignore", False),
        )
        return f"Mouse from {cur_pos} dragged to ({x}, {y}) with duration {duration} ms"

    def __dissolve_click(self, mouse: Mouse) -> str:
        cur_x, cur_y = InputController.get_mouse_position()
        x: Optional[int] = mouse.get("x", None)
        y: Optional[int] = mouse.get("y", None)
        if x is None and y is None:
            x = cur_x
            y = cur_y
        elif mouse.get("relative", False):
            x = x or cur_x
            y = y or cur_y
            x += cur_x
            y += cur_y

        duration = mouse.get("duration", 0)
        button = mouse.get("button", "LEFT")
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )

        InputController.mouse_click_at(
            button=button.lower(),
            x=x,
            y=y,
            duration=duration,
            debug=self.globals.get("debug", False),
            ignore=self.globals.get("ignore", False),
        )
        return f"Mouse clicked at ({x}, {y}) with duration {duration} ms"

    def execute_MouseInput(self, mouse: Mouse) -> str:
        mt = mouse.get("type")
        if mt in {"Press", "Release"}:
            return self.__dissolve_event(mouse)
        elif mt == "Move":
            return self.__dissolve_move(mouse)
        elif mt == "Drag":
            return self.__dissolve_drag(mouse)
        elif mt == "Click":
            return self.__dissolve_click(mouse)
        else:
            raise ActionTypeError(f"Unsupported mouse action type: {mt}", self.job)

    def execute_KeyboardInput(self, keyboard: Keyboard) -> str:
        tp = keyboard.get("type")
        if tp not in {"Press", "Release", "Type"}:
            raise ActionTypeError(f"Unsupported keyboard action type: {tp}", self.job)

        keys = keyboard.get("keys", None)
        if tp == "Press":
            InputController.keyboard_press(
                keys,
                debug=self.globals.get("debug", False),
            )
            return f"Keyboard pressed: {keyboard.get('keys', [])}"
        elif tp == "Release":
            InputController.keyboard_release(
                keys,
                debug=self.globals.get("debug", False),
            )
            return f"Keyboard released: {keyboard.get('keys', [])}"
        # tp == Type
        duration = keyboard.get("duration", 0)
        sep_time = keyboard.get("sep_time", 0)

        InputController.keyboard_press_and_release(
            keys,
            duration=duration,
            sep_time=sep_time,
            debug=self.globals.get("debug", False),
        )
        return f"Keyboard typed: {keys} with duration {duration} ms"

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
