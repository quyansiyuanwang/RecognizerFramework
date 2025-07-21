from typing import Any, Dict, Final, Optional, Set

from ...Structure import Keyboard, Mouse, Text
from ...Typehints import GlobalsDict, TaskReturnsDict
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
        self.use_vars: Dict[str, Any] = {}

    def execute_TextInput(self, text: Text) -> TaskReturnsDict[str]:
        text.update(self.use_vars)
        message = text.get("message", "")
        duration = text.get("duration", 0)

        InputController.typewrite(
            message, duration=duration, debug=self.globals.get("debug", False)
        )
        return TaskReturnsDict(
            returns=text.get("returns", {}),
            variables={"message": message, "duration": duration},
            result=f"Typed input: {message} with duration {duration} ms",
        )

    def __dissolve_event(self, mouse: Mouse) -> TaskReturnsDict[str]:
        mouse.update(self.use_vars)
        button = mouse.get("button", "LEFT")
        duration = mouse.get("duration", 0)
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )
        mt = mouse.get("type")
        InputController.mouse_event(
            mt,
            button=button.lower(),
            duration=duration,
            debug=self.globals.get("debug", False),
        )
        return TaskReturnsDict(
            returns=mouse.get("returns", {}),
            variables={"button": button, "type": mt, "duration": duration},
            result=f"{button} mouse button {mt.lower()}ed",
        )

    def __dissolve_move(self, mouse: Mouse) -> TaskReturnsDict[str]:
        mouse.update(self.use_vars)
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

        InputController.mouse_move_to(
            x,
            y,
            duration=duration,
            debug=self.globals.get("debug", False),
            ignore=self.globals.get("ignore", False),
        )

        return TaskReturnsDict(
            returns=mouse.get("returns", {}),
            variables={
                "origin_x": cur_pos[0],
                "origin_y": cur_pos[1],
                "x": x,
                "y": y,
                "duration": duration,
            },
            result=f"Mouse moved to ({x}, {y}) with duration {duration} ms",
        )

    def __dissolve_drag(self, mouse: Mouse) -> TaskReturnsDict[str]:
        mouse.update(self.use_vars)
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
        return TaskReturnsDict(
            returns=mouse.get("returns", {}),
            variables={
                "origin_x": cur_pos[0],
                "origin_y": cur_pos[1],
                "x": x,
                "y": y,
                "duration": duration,
            },
            result=f"Mouse from {cur_pos} dragged to ({x}, {y}) with duration {duration} ms",
        )

    def __dissolve_click(self, mouse: Mouse) -> TaskReturnsDict[str]:
        mouse.update(self.use_vars)
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
        return TaskReturnsDict(
            returns=mouse.get("returns", {}),
            variables={
                "origin_x": cur_x,
                "origin_y": cur_y,
                "x": x,
                "y": y,
                "duration": duration,
            },
            result=f"Mouse clicked at ({x}, {y}) with duration {duration} ms",
        )

    def execute_MouseInput(self, mouse: Mouse) -> TaskReturnsDict[str]:
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

    def execute_KeyboardInput(self, keyboard: Keyboard) -> TaskReturnsDict[str]:
        keyboard.update(self.use_vars)
        tp = keyboard.get("type")
        if tp not in {"Press", "Release", "Type"}:
            raise ActionTypeError(f"Unsupported keyboard action type: {tp}", self.job)

        keys = keyboard.get("keys", None)
        if tp == "Press":
            InputController.keyboard_press(
                keys,
                debug=self.globals.get("debug", False),
            )
            return TaskReturnsDict(
                returns=keyboard.get("returns", {}),
                variables={"keys": keys, "type": tp},
                result=f"Keyboard pressed: {keyboard.get('keys', [])}",
            )
        elif tp == "Release":
            InputController.keyboard_release(
                keys,
                debug=self.globals.get("debug", False),
            )
            return TaskReturnsDict(
                returns=keyboard.get("returns", {}),
                variables={"keys": keys, "type": tp},
                result=f"Keyboard released: {keyboard.get('keys', [])}",
            )
        # tp == Type
        duration = keyboard.get("duration", 0)
        sep_time = keyboard.get("sep_time", 0)

        InputController.keyboard_press_and_release(
            keys,
            duration=duration,
            sep_time=sep_time,
            debug=self.globals.get("debug", False),
        )
        return TaskReturnsDict(
            returns=keyboard.get("returns", {}),
            variables={"keys": keys, "type": tp, "duration": duration},
            result=f"Keyboard typed: {keys} with duration {duration} ms",
        )

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[str]:
        self.use_vars.update(kwargs)
        inp = self.job.get("input", {})
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
