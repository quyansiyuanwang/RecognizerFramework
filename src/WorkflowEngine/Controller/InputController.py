from typing import List

import keyboard
import pyautogui
import pyperclip  # type: ignore[import-untyped]
import pywinauto  # type: ignore[import-not-found]

from .Runner import SafeRunner
from .SystemController import SystemController


class InputController:
    @staticmethod
    def click(
        x: int,
        y: int,
        delay_ms: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        SafeRunner.run(
            pyautogui.click,
            (x, y),
            {},
            ignore=ignore,
            debug=debug,
            # logger
            debug_msg=f"Clicking at ({x}, {y}) with delay {delay_ms} ms",
            warn_msg=f"Failed to click at ({x}, {y}) with delay {delay_ms} ms",
            err_msg=f"Error clicking at ({x}, {y}) with delay {delay_ms} ms: {{error}}",
        )

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
        delay_ms: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        for k in keys:
            InputController.keyboard_press(k, debug=debug, ignore=ignore)
        SystemController.sleep(
            delay_ms,
            debug=debug,
            ignore=ignore,
            prefix="InputControllerPressCurDelay",
        )
        for k in reversed(keys):
            InputController.keyboard_release(k, debug=debug, ignore=ignore)
