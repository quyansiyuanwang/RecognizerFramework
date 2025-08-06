from typing import Callable, Dict, List, Literal, Optional, Tuple

import keyboard
import pyautogui
import pywinauto  # type: ignore[import-untyped]

from .Runner import SafeRunner
from .SystemController import SystemController

pyautogui.PAUSE = 0  # Disable default pause between actions
pyautogui.FAILSAFE = False  # Disable fail-safe to prevent mouse movement issues


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

    @staticmethod
    def keyboard_press(
        keys: List[str],
        sep_time: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        if hWnd is not None:
            # 后台按键输入到指定窗口
            for key in keys:
                # 将字符串键转换为虚拟键码
                key_code = InputController._key_to_vk_code(key)
                if key_code:
                    InputController._virtual_key_to_window(
                        hWnd, key_code, "keydown", debug, ignore
                    )
                SystemController.sleep(sep_time, debug=debug, ignore=ignore)
        else:
            # 前台按键输入
            for key in keys:
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
                SystemController.sleep(sep_time, debug=debug, ignore=ignore)

    @staticmethod
    def keyboard_release(
        keys: List[str],
        sep_time: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        for key in keys:
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
            SystemController.sleep(sep_time, debug=debug, ignore=ignore)

    @staticmethod
    def keyboard_press_and_release(
        keys: List[str],
        duration: int = 0,
        sep_time: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        InputController.keyboard_press(
            keys, sep_time=sep_time, debug=debug, ignore=ignore
        )

        SystemController.sleep(
            duration,
            debug=debug,
            ignore=ignore,
            prefix="InputControllerPressDurationDelay",
        )
        InputController.keyboard_release(
            list(reversed(keys)), sep_time=sep_time, debug=debug, ignore=ignore
        )

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
        duration: int = 0,
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
            {"button": button.lower(), "duration": duration / 1000},
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
        hWnd: Optional[int] = None,
    ):
        if hWnd is not None and x is not None and y is not None:
            # 后台鼠标拖拽 - 需要先按下，移动，然后释放
            try:
                lParam = input_controller_util.trans_lParam(x, y)

                button_map = {
                    "LEFT": (win32con.WM_LBUTTONDOWN, win32con.WM_LBUTTONUP),
                    "RIGHT": (win32con.WM_RBUTTONDOWN, win32con.WM_RBUTTONUP),
                    "MIDDLE": (win32con.WM_MBUTTONDOWN, win32con.WM_MBUTTONUP),
                }

                down_msg, up_msg = button_map[button]

                # 发送鼠标按下消息
                InputController._send_message_to_window(
                    hWnd, down_msg, 0, lParam, debug, ignore
                )

                # 发送鼠标移动消息
                InputController._send_message_to_window(
                    hWnd, win32con.WM_MOUSEMOVE, 0, lParam, debug, ignore
                )

                # 发送鼠标抬起消息
                InputController._send_message_to_window(
                    hWnd, up_msg, 0, lParam, debug, ignore
                )

            except Exception as e:
                if not ignore:
                    raise RuntimeError(
                        f"Failed to drag to ({x}, {y}) in window {hWnd}: {e}"
                    ) from e
        else:
            # 前台鼠标拖拽
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

    # 辅助方法：获取窗口句柄
    @staticmethod
    def get_window_handle_by_title(
        title: str, exact_match: bool = False
    ) -> Optional[int]:
        """
        根据窗口标题获取窗口句柄
        """

        def enum_windows_callback(hWnd: int, windows: List[Tuple[int, str]]) -> bool:
            if win32gui.IsWindowVisible(hWnd):
                window_title = win32gui.GetWindowText(hWnd)
                if exact_match:
                    if window_title == title:
                        windows.append((hWnd, window_title))
                else:
                    if title.lower() in window_title.lower():
                        windows.append((hWnd, window_title))
            return True

        windows: List[Tuple[int, str]] = []
        win32gui.EnumWindows(enum_windows_callback, windows)

        return windows[0][0] if windows else None

    @staticmethod
    def get_window_handle_by_class(class_name: str) -> Optional[int]:
        """
        根据窗口类名获取窗口句柄
        """
        try:
            hWnd = win32gui.FindWindow(class_name, None)
            return hWnd if hWnd != 0 else None
        except Exception:
            return None

    @staticmethod
    def send_text_no_focus_change(
        hWnd: int,
        text: str,
        method: Literal["wm_char", "wm_settext", "clipboard"] = "wm_char",
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        """
        发送文本到窗口，确保不改变焦点

        Args:
            hWnd: 目标窗口句柄
            text: 要发送的文本
            method: 发送方式
                - "wm_char": 逐字符发送 WM_CHAR 消息（适用于大多数输入框）
                - "wm_settext": 直接设置窗口文本（适用于简单文本框）
                - "clipboard": 通过剪贴板粘贴（适用于复杂应用）
        """

        try:
            if method == "wm_char":
                # 逐字符发送 WM_CHAR 消息
                for char in text:
                    InputController._send_message_to_window(
                        hWnd, win32con.WM_CHAR, ord(char), 0, debug, ignore
                    )

            elif method == "wm_settext":
                # 直接设置窗口文本 - 注意：某些应用可能不支持此方法
                try:
                    win32gui.SetWindowText(hWnd, text)  # type: ignore[call-arg]
                except Exception:
                    # 如果失败，回退到 WM_CHAR 方法
                    for char in text:
                        InputController._send_message_to_window(
                            hWnd, win32con.WM_CHAR, ord(char), 0, debug, ignore
                        )

            elif method == "clipboard":
                # 保存当前剪贴板内容
                old_clipboard = input_controller_util.get_clipboard()

                # 发送 Ctrl+V 到目标窗口
                InputController._send_message_to_window(
                    hWnd, win32con.WM_KEYDOWN, win32con.VK_CONTROL, 0, debug, ignore
                )
                InputController._send_message_to_window(
                    hWnd, win32con.WM_KEYDOWN, ord("V"), 0, debug, ignore
                )
                InputController._send_message_to_window(
                    hWnd, win32con.WM_KEYUP, ord("V"), 0, debug, ignore
                )
                InputController._send_message_to_window(
                    hWnd, win32con.WM_KEYUP, win32con.VK_CONTROL, 0, debug, ignore
                )

                # 恢复原剪贴板内容
                if old_clipboard:
                    input_controller_util.set_clipboard(old_clipboard)

        except Exception as e:
            if not ignore:
                raise RuntimeError(
                    f"Failed to send text '{text}' to window {hWnd} using method {method}: {e}"
                ) from e

    @staticmethod
    def get_current_foreground_window() -> Optional[int]:
        """
        获取当前前台窗口句柄
        """
        try:
            return win32gui.GetForegroundWindow()
        except Exception:
            return None

    @staticmethod
    def is_window_focused(hWnd: int) -> bool:
        """
        检查指定窗口是否获得焦点
        """
        try:
            return win32gui.GetForegroundWindow() == hWnd
        except Exception:
            return False

    # 私有辅助方法
    @staticmethod
    def _send_message_to_window(
        hWnd: int,
        message: int,
        wParam: int = 0,
        lParam: int = 0,
        debug: bool = True,
        ignore: bool = False,
    ) -> Optional[int]:
        """
        向指定窗口发送Windows消息
        """
        try:
            result = SafeRunner.run(
                win32gui.SendMessage,
                (hWnd, message, wParam, lParam),
                {},
                ignore=ignore,
                debug=debug,
                # logger
                debug_msg=f"Sending message {message} to window {hWnd}",
                warn_msg=f"Failed to send message {message} to window {hWnd}",
                err_msg=f"Error sending message {message} to window {hWnd}: {{error}}",
            )
            return result
        except Exception as e:
            if not ignore:
                raise RuntimeError(
                    f"Failed to send message {message} to window {hWnd}: {e}"
                ) from e
            return None

    @staticmethod
    def _virtual_key_to_window(
        hWnd: int,
        key_code: int,
        event_type: Literal["keydown", "keyup"],
        debug: bool = True,
        ignore: bool = False,
    ) -> None:
        """
        向指定窗口发送虚拟按键消息
        """
        try:
            if event_type == "keydown":
                InputController._send_message_to_window(
                    hWnd, win32con.WM_KEYDOWN, key_code, 0, debug, ignore
                )

            if event_type == "keyup":
                InputController._send_message_to_window(
                    hWnd, win32con.WM_KEYUP, key_code, 0, debug, ignore
                )

        except Exception as e:
            if not ignore:
                raise RuntimeError(
                    f"Failed to send key {key_code} to window {hWnd}: {e}"
                ) from e

    @staticmethod
    def _key_to_vk_code(key: str) -> Optional[int]:
        """
        将字符串键名转换为虚拟键码，使用现成的工具函数
        """
        return input_controller_util.key_name_to_vk_code(key)
