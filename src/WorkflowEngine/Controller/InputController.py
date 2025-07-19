from typing import Callable, Dict, List, Literal, Optional, Tuple

import keyboard
import pyautogui
import pyperclip  # type: ignore[import-untyped]
import pywinauto  # type: ignore[import-untyped]

from .Runner import SafeRunner
from .SystemController import SystemController

pyautogui.PAUSE = 0  # Disable default pause between actions


class InputController:
    @staticmethod
    def get_mouse_position() -> Tuple[int, int]:
        return pyautogui.position()

    @staticmethod
    def typewrite(
        text: str,
        duration: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        try:
            SafeRunner.run(
                pywinauto.keyboard.send_keys,  # type: ignore[no-untyped-call]
                (text,),
                {"with_spaces": True, "pause": duration / 1000 / len(text)},
                ignore=ignore,
                debug=debug,
                # logger
                debug_msg=f"Typing text: '{text}' in {duration} ms",
                warn_msg=f"Failed to typewrite '{text}' with delay {duration} ms",
                err_msg=f"Error typing '{text}' with delay {duration} ms: {{error}}",
            )
        except Exception as e:
            if not ignore:
                raise RuntimeError(f"Failed to typewrite '{text}': {e}") from e

            SafeRunner.run(
                pyperclip.copy,
                (text,),
                {},
                ignore=ignore,
                debug=debug,
                # logger
                debug_msg=f"Falling back to clipboard paste for text: '{text}'",
                warn_msg=f"Failed to copy text '{text}' to clipboard",
                err_msg=f"Error copying text '{text}' to clipboard: {{error}}",
            )
            SafeRunner.run(
                pyautogui.hotkey,
                ("ctrl", "v"),
                {},
                ignore=ignore,
                debug=debug,
                # logger
                debug_msg=f"Pasting text from clipboard: '{text}'",
                warn_msg=f"Failed to paste text from clipboard: '{text}'",
                err_msg=f"Error pasting text from clipboard: {{error}}",
            )

    @staticmethod
    def keyboard_press(
        key: str,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        SafeRunner.run(
            keyboard.press,
            (key,),
            {},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"Keyboard input: '{key}'",
            warn_msg=f"Failed to keyboard input '{key}'",
            err_msg=f"Error keyboard input '{key}': {{error}}",
        )

    @staticmethod
    def keyboard_release(
        key: str,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        SafeRunner.run(
            keyboard.release,
            (key,),
            {},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"Keyboard release: '{key}'",
            warn_msg=f"Failed to release keyboard '{key}'",
            err_msg=f"Error releasing keyboard '{key}': {{error}}",
        )

    @staticmethod
    def keyboard_press_and_release(
        keys: List[str],
        duration: int = 0,
        sep_time: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        for k in keys:
            InputController.keyboard_press(k, debug=debug, ignore=ignore)
            SystemController.sleep(
                sep_time,
                debug=debug,
                ignore=ignore,
                prefix="InputControllerPressSepDelay",
            )

        SystemController.sleep(
            duration,
            debug=debug,
            ignore=ignore,
            prefix="InputControllerPressDurationDelay",
        )
        for k in reversed(keys):
            InputController.keyboard_release(k, debug=debug, ignore=ignore)

    @staticmethod
    def mouse_move_to(
        x: int,
        y: int,
        duration: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        SafeRunner.run(
            pyautogui.moveTo,
            (x, y),
            {"duration": duration / 1000},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"Moving mouse to ({x}, {y}) with delay {duration} ms",
            warn_msg=f"Failed to move mouse to ({x}, {y}) with delay {duration} ms",
            err_msg=f"Error moving mouse to ({x}, {y}) with delay {duration} ms: {{error}}",
        )

    @staticmethod
    def mouse_event(
        event_type: Literal["Press", "Release"],
        button: Literal["LEFT", "RIGHT", "MIDDLE"] = "LEFT",
        debug: bool = True,
        ignore: bool = False,
    ):
        fnc_map: Dict[str, Callable[..., None]] = {
            "Press": pyautogui.mouseDown,
            "Release": pyautogui.mouseUp,
        }
        SafeRunner.run(
            fnc_map[event_type],
            (),
            {"button": button.lower()},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"{event_type.capitalize()} mouse button: {button}",
            warn_msg=f"Failed to {event_type.lower()} mouse button: {button}",
            err_msg=f"Error {event_type.lower()} mouse button: {button}: {{error}}",
        )

    @staticmethod
    def mouse_click_at(
        button: Literal["LEFT", "RIGHT", "MIDDLE"] = "LEFT",
        x: Optional[int] = None,
        y: Optional[int] = None,
        duration: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        SafeRunner.run(
            pyautogui.click,
            (x, y) if x is not None and y is not None else (),
            {"button": button.lower(), "duration": duration / 1000},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"Clicking mouse button {button} at ({x}, {y}) with delay {duration} ms",
            warn_msg=f"Failed to click mouse button {button} at ({x}, {y}) with delay {duration} ms",
            err_msg=f"Error clicking mouse button {button} at ({x}, {y}) with delay {duration} ms: {{error}}",
        )

    @staticmethod
    def mouse_drag_to(
        button: Literal["LEFT", "RIGHT", "MIDDLE"] = "LEFT",
        x: Optional[int] = None,
        y: Optional[int] = None,
        duration: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ):
        SafeRunner.run(
            pyautogui.dragTo,
            (x, y) if x is not None and y is not None else (),
            {"button": button.lower(), "duration": duration / 1000},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"Dragging mouse to ({x}, {y}) with button {button} and delay {duration} ms",
            warn_msg=f"Failed to drag mouse to ({x}, {y}) with button {button} and delay {duration} ms",
            err_msg=f"Error dragging mouse to ({x}, {y}) with button {button} and delay {duration} ms: {{error}}",
        )
