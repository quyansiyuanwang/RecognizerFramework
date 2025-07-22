from typing import Any, Dict, Final, Literal, Set, cast

from src.WorkflowEngine.Util.executor_works import update

from ...Typehints import (
    Globals,
    Input_Keyboard,
    Input_Mouse,
    Input_Text,
    TaskReturnsDict,
)
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
    def __init__(self, job: Job, globals: Globals) -> None:
        self.job: Job = job
        self.globals: Globals = globals
        self.use_vars: Dict[str, Any] = {}

    def execute_TextInput(self, text: Input_Text) -> TaskReturnsDict[str]:
        update(text, self.use_vars)
        message = text.message
        duration = text.duration

        InputController.typewrite(
            message,
            duration=duration,
            debug=self.globals.model_dump().get("debug", False),
        )
        return TaskReturnsDict(
            returns=cast(Dict[str, str], text.returns),
            variables={"message": message, "duration": duration},
            result=f"Typed input: {message} with duration {duration} ms",
        )

    def __dissolve_event(self, mouse: Input_Mouse) -> TaskReturnsDict[str]:
        update(mouse, self.use_vars)
        button = mouse.button
        duration = mouse.duration
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )
        mt = mouse.type
        InputController.mouse_event(
            cast(Literal["Press", "Release"], mt),
            button=button,
            duration=duration,
            debug=self.globals.debug,
        )
        return TaskReturnsDict(
            returns=cast(Dict[str, str], mouse.returns),
            variables={"button": button, "type": mt, "duration": duration},
            result=f"{button} mouse button {mt.lower()}ed",
        )

    def __dissolve_move(self, mouse: Input_Mouse) -> TaskReturnsDict[str]:
        update(mouse, self.use_vars)
        if not (mouse.x or mouse.y):
            raise MouseMovePositionError("Missing required any of keys: x, y", self.job)

        x: int = mouse.x
        y: int = mouse.y
        duration = mouse.duration
        relative = mouse.relative
        button = mouse.button
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
            debug=self.globals.debug,
            ignore=self.globals.ignore,
        )

        return TaskReturnsDict(
            returns=cast(Dict[str, str], mouse.returns),
            variables={
                "origin_x": cur_pos[0],
                "origin_y": cur_pos[1],
                "x": x,
                "y": y,
                "duration": duration,
            },
            result=f"Mouse moved to ({x}, {y}) with duration {duration} ms",
        )

    def __dissolve_drag(self, mouse: Input_Mouse) -> TaskReturnsDict[str]:
        update(mouse, self.use_vars)
        if not (mouse.x or mouse.y):
            raise MouseMovePositionError("Missing required any of keys: x, y", self.job)

        x: int = mouse.x
        y: int = mouse.y
        duration = mouse.duration
        relative = mouse.relative
        button = mouse.button
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
            button=button,
            x=x,
            y=y,
            duration=duration,
            debug=self.globals.debug,
            ignore=self.globals.ignore,
        )
        return TaskReturnsDict(
            returns=cast(Dict[str, str], mouse.returns),
            variables={
                "origin_x": cur_pos[0],
                "origin_y": cur_pos[1],
                "x": x,
                "y": y,
                "duration": duration,
            },
            result=f"Mouse from {cur_pos} dragged to ({x}, {y}) with duration {duration} ms",
        )

    def __dissolve_click(self, mouse: Input_Mouse) -> TaskReturnsDict[str]:
        update(mouse, self.use_vars)
        cur_x, cur_y = InputController.get_mouse_position()
        x: int = mouse.x
        y: int = mouse.y
        if not x and not y:
            x = cur_x
            y = cur_y
        elif mouse.relative:
            x = x or cur_x
            y = y or cur_y
            x += cur_x
            y += cur_y

        duration = mouse.duration
        button = mouse.button
        if button not in AVAILABLE_MOUSE_BUTTONS:
            raise ActionTypeError(
                f"Unsupported mouse button: {button}. Available: {AVAILABLE_MOUSE_BUTTONS}",
                self.job,
            )

        InputController.mouse_click_at(
            button=button,
            x=x,
            y=y,
            duration=duration,
            debug=self.globals.debug,
            ignore=self.globals.ignore,
        )
        return TaskReturnsDict(
            returns=cast(Dict[str, str], mouse.returns),
            variables={
                "origin_x": cur_x,
                "origin_y": cur_y,
                "x": x,
                "y": y,
                "duration": duration,
            },
            result=f"Mouse clicked at ({x}, {y}) with duration {duration} ms",
        )

    def execute_MouseInput(self, mouse: Input_Mouse) -> TaskReturnsDict[str]:
        mt = mouse.type
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

    def execute_KeyboardInput(self, keyboard: Input_Keyboard) -> TaskReturnsDict[str]:
        update(keyboard, self.use_vars)
        tp = keyboard.type
        if tp not in {"Press", "Release", "Type"}:
            raise ActionTypeError(f"Unsupported keyboard action type: {tp}", self.job)

        keys = keyboard.keys
        if tp == "Press":
            InputController.keyboard_press(
                keys,
                debug=self.globals.debug,
            )
            return TaskReturnsDict(
                returns=cast(Dict[str, str], keyboard.returns),
                variables={"keys": keys, "type": tp},
                result=f"Keyboard pressed: {keyboard.keys}",
            )
        elif tp == "Release":
            InputController.keyboard_release(
                keys,
                debug=self.globals.debug,
            )
            return TaskReturnsDict(
                returns=cast(Dict[str, str], keyboard.returns),
                variables={"keys": keys, "type": tp},
                result=f"Keyboard released: {keyboard.keys}",
            )
        # tp == Type
        duration = keyboard.duration
        sep_time = keyboard.sep_time

        InputController.keyboard_press_and_release(
            keys,
            duration=duration,
            sep_time=sep_time,
            debug=self.globals.debug,
        )
        return TaskReturnsDict(
            returns=cast(Dict[str, str], keyboard.returns),
            variables={"keys": keys, "type": tp, "duration": duration},
            result=f"Keyboard typed: {keys} with duration {duration} ms",
        )

    def execute(self, *args: Any, **kwargs: Any) -> TaskReturnsDict[str]:
        self.use_vars.update(kwargs)
        inp = self.job.input
        if not inp:
            raise MissingRequiredError(
                "No input found in the job to execute.", self.job
            )

        if inp.type == "Text" and inp.text:
            return self.execute_TextInput(inp.text)
        elif inp.type == "Mouse" and inp.mouse:
            return self.execute_MouseInput(inp.mouse)
        elif inp.type == "Keyboard" and inp.keyboard:
            return self.execute_KeyboardInput(inp.keyboard)
        else:
            raise ActionTypeError(
                f"Unsupported input type({inp.type}) or missing field({inp.type.lower()})",
                self.job,
            )
