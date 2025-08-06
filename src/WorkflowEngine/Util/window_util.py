from typing import List, Optional

import win32api
import win32con
import win32gui
import win32process

from ..Exceptions.crash import MissingRequiredError


class WindowUtil:
    """窗口工具类，提供窗口查找和操作功能"""

    @staticmethod
    def find_window(
        title: Optional[str] = None,
        class_name: Optional[str] = None,
        process: Optional[str] = None,
        exact: bool = False,
        visible_only: bool = True,
    ) -> List[int]:
        """
        根据条件查找窗口句柄

        Args:
            title: 窗口标题
            class_name: 窗口类名
            process: 进程名

        Returns:
            int: 窗口句柄

        Raises:
            MissingRequiredError: 如果没有提供任何查找条件
            WindowNotFoundError: 如果未找到匹配的窗口
            MultipleMatchedError: 如果匹配到多个窗口
        """
        if not (title or class_name or process):
            raise MissingRequiredError(
                "At least one of title, class_name or process must be specified."
            )

        # 获取所有窗口的句柄
        def hwnd_callback(hWnd: int, param: List[int]) -> None:
            param.append(hWnd)

        hWnd_list: List[int] = []
        matched: List[int] = []
        win32gui.EnumWindows(hwnd_callback, hWnd_list)

        for hWnd in hWnd_list:
            # 窗口过滤
            if not win32gui.IsWindowVisible(hWnd):
                continue

            # 获取窗口标题
            window_title: str = win32gui.GetWindowText(hWnd)
            if not window_title:
                continue

            # 获取窗口类名
            window_class_name: Optional[str] = win32gui.GetClassName(hWnd)

            # 获取进程信息
            process_id = win32process.GetWindowThreadProcessId(hWnd)[1]
            h_process = win32api.OpenProcess(
                win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ,
                False,
                process_id,
            )
            path: str = str(win32process.GetModuleFileNameEx(h_process, 0))  # type: ignore[union-attr]
            window_process: str = path.split("\\")[-1] if path else ""
            win32api.CloseHandle(h_process)

            # 匹配条件检查, exact参数用于精确匹配
            title_match = not title or (
                window_title == title if exact else title in window_title
            )
            class_match = not class_name or (
                window_class_name == class_name
                if exact
                else (window_class_name and class_name in window_class_name)
            )
            process_match = not process or (
                window_process == process if exact else process in window_process
            )
            visible_match = win32gui.IsWindowVisible(hWnd) if visible_only else True
            if title_match and class_match and process_match and visible_match:
                matched.append(hWnd)

        return matched

    @staticmethod
    def get_focused_window() -> Optional[int]:
        """
        获取当前焦点窗口的句柄

        Returns:
            int: 当前焦点窗口的句柄，如果没有焦点窗口则返回 None
        """
        return win32gui.GetForegroundWindow()

    @staticmethod
    def focus_window_by_handle(hWnd: int) -> None:
        """
        设置指定窗口为焦点窗口

        Args:
            hWnd: 窗口句柄
        """
        win32gui.SetForegroundWindow(hWnd)
