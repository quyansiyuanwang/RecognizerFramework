from typing import Optional

import win32api
import win32clipboard
import win32con

from .key_mapper import key_name_to_vk_code as _key_mapper_func


def trans_lParam(x: int, y: int) -> int:
    return win32api.MAKELONG(x, y)  # type: ignore[attr-defined]


def set_clipboard(text: str) -> None:
    win32clipboard.OpenClipboard()  # type: ignore[no-untyped-call]
    win32clipboard.EmptyClipboard()  # type: ignore[no-untyped-call]
    win32clipboard.SetClipboardData(win32con.CF_TEXT, text.encode("utf-8"))  # type: ignore[no-untyped-call]
    win32clipboard.CloseClipboard()  # type: ignore[no-untyped-call]


def get_clipboard() -> str:
    win32clipboard.OpenClipboard()  # type: ignore[no-untyped-call]
    try:
        return win32clipboard.GetClipboardData(win32con.CF_TEXT).decode("utf-8")  # type: ignore[no-untyped-call]
    except TypeError:
        return ""
    finally:
        win32clipboard.CloseClipboard()  # type: ignore[no-untyped-call]


def key_name_to_vk_code(key_name: str) -> Optional[int]:
    """
    将键名转换为虚拟键码，使用专门的键映射器
    """
    return _key_mapper_func(key_name)
