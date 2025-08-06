"""
键名映射工具 - 提供现成的键名到虚拟键码的映射
"""

from typing import Dict, List, Optional

import win32con


class KeyMapper:
    """键名到虚拟键码的映射器"""

    # 标准的键名映射表
    _KEY_MAP: Dict[str, int] = {
        # 字母键 (A-Z)
        "a": ord("A"),
        "b": ord("B"),
        "c": ord("C"),
        "d": ord("D"),
        "e": ord("E"),
        "f": ord("F"),
        "g": ord("G"),
        "h": ord("H"),
        "i": ord("I"),
        "j": ord("J"),
        "k": ord("K"),
        "l": ord("L"),
        "m": ord("M"),
        "n": ord("N"),
        "o": ord("O"),
        "p": ord("P"),
        "q": ord("Q"),
        "r": ord("R"),
        "s": ord("S"),
        "t": ord("T"),
        "u": ord("U"),
        "v": ord("V"),
        "w": ord("W"),
        "x": ord("X"),
        "y": ord("Y"),
        "z": ord("Z"),
        # 数字键 (0-9)
        "0": ord("0"),
        "1": ord("1"),
        "2": ord("2"),
        "3": ord("3"),
        "4": ord("4"),
        "5": ord("5"),
        "6": ord("6"),
        "7": ord("7"),
        "8": ord("8"),
        "9": ord("9"),
        # 特殊键
        "enter": win32con.VK_RETURN,
        "return": win32con.VK_RETURN,
        "space": win32con.VK_SPACE,
        "tab": win32con.VK_TAB,
        "escape": win32con.VK_ESCAPE,
        "esc": win32con.VK_ESCAPE,
        "shift": win32con.VK_SHIFT,
        "ctrl": win32con.VK_CONTROL,
        "control": win32con.VK_CONTROL,
        "alt": win32con.VK_MENU,
        "backspace": win32con.VK_BACK,
        "delete": win32con.VK_DELETE,
        "del": win32con.VK_DELETE,
        "home": win32con.VK_HOME,
        "end": win32con.VK_END,
        "pageup": win32con.VK_PRIOR,
        "pagedown": win32con.VK_NEXT,
        "up": win32con.VK_UP,
        "down": win32con.VK_DOWN,
        "left": win32con.VK_LEFT,
        "right": win32con.VK_RIGHT,
        "insert": win32con.VK_INSERT,
        "caps": win32con.VK_CAPITAL,
        "capslock": win32con.VK_CAPITAL,
        "numlock": win32con.VK_NUMLOCK,
        "scrolllock": win32con.VK_SCROLL,
        "pause": win32con.VK_PAUSE,
        "printscreen": win32con.VK_SNAPSHOT,
        "win": win32con.VK_LWIN,
        "lwin": win32con.VK_LWIN,
        "rwin": win32con.VK_RWIN,
        "menu": win32con.VK_APPS,
        # 功能键
        "f1": win32con.VK_F1,
        "f2": win32con.VK_F2,
        "f3": win32con.VK_F3,
        "f4": win32con.VK_F4,
        "f5": win32con.VK_F5,
        "f6": win32con.VK_F6,
        "f7": win32con.VK_F7,
        "f8": win32con.VK_F8,
        "f9": win32con.VK_F9,
        "f10": win32con.VK_F10,
        "f11": win32con.VK_F11,
        "f12": win32con.VK_F12,
        # 数字键盘
        "num0": win32con.VK_NUMPAD0,
        "num1": win32con.VK_NUMPAD1,
        "num2": win32con.VK_NUMPAD2,
        "num3": win32con.VK_NUMPAD3,
        "num4": win32con.VK_NUMPAD4,
        "num5": win32con.VK_NUMPAD5,
        "num6": win32con.VK_NUMPAD6,
        "num7": win32con.VK_NUMPAD7,
        "num8": win32con.VK_NUMPAD8,
        "num9": win32con.VK_NUMPAD9,
        "decimal": win32con.VK_DECIMAL,
        "divide": win32con.VK_DIVIDE,
        "multiply": win32con.VK_MULTIPLY,
        "subtract": win32con.VK_SUBTRACT,
        "add": win32con.VK_ADD,
    }

    @classmethod
    def get_vk_code(cls, key_name: str) -> Optional[int]:
        """
        根据键名获取虚拟键码

        Args:
            key_name: 键名（不区分大小写）

        Returns:
            虚拟键码，如果找不到则返回 None
        """
        key_lower = key_name.lower()
        return cls._KEY_MAP.get(key_lower)

    @classmethod
    def is_valid_key(cls, key_name: str) -> bool:
        """
        检查键名是否有效

        Args:
            key_name: 键名

        Returns:
            如果键名有效返回 True，否则返回 False
        """
        return cls.get_vk_code(key_name) is not None

    @classmethod
    def get_all_keys(cls) -> List[str]:
        """
        获取所有支持的键名列表

        Returns:
            所有支持的键名列表
        """
        return list(cls._KEY_MAP.keys())


# 提供简单的函数接口
def key_name_to_vk_code(key_name: str) -> Optional[int]:
    """
    将键名转换为虚拟键码

    Args:
        key_name: 键名（不区分大小写）

    Returns:
        虚拟键码，如果找不到则返回 None

    Examples:
        >>> key_name_to_vk_code("enter")
        13
        >>> key_name_to_vk_code("a")
        65
        >>> key_name_to_vk_code("f1")
        112
    """
    return KeyMapper.get_vk_code(key_name)


def is_valid_key_name(key_name: str) -> bool:
    """
    检查键名是否有效

    Args:
        key_name: 键名

    Returns:
        如果键名有效返回 True，否则返回 False
    """
    return KeyMapper.is_valid_key(key_name)


def get_supported_keys() -> List[str]:
    """
    获取所有支持的键名列表

    Returns:
        所有支持的键名列表
    """
    return KeyMapper.get_all_keys()
