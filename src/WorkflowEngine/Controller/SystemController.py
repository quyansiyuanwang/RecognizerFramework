import subprocess
import time
from typing import Dict, List, Optional

import pyautogui
import pyperclip  # type: ignore[import-untyped]

from .LogController import LogLevel
from .Runner import SafeRunner


class SystemController:
    @staticmethod
    def sleep(
        ms: float,
        debug: bool = True,
        ignore: bool = False,
        prefix: str = "",
        levels: List[LogLevel] = [LogLevel.DEBUG],
    ) -> None:
        if ms <= 0:
            if ignore or ms == 0:
                return
            raise ValueError("Sleep duration must be non-negative")

        SafeRunner.run(
            time.sleep,
            (ms / 1000,),
            debug=debug,
            ignore=ignore,
            # logger
            context={"ms": ms},
            debug_msg=f"{prefix} Sleeping for {ms} ms",
            warn_msg=f"{prefix} Failed to sleep for {ms} ms",
            err_msg=f"{prefix} Error sleeping for {ms} ms: {{error}}",
            log_lvl=levels,
        )

    @staticmethod
    def paste() -> str:
        content = pyperclip.paste()

        def perform_paste() -> None:
            pyperclip.copy(content)
            pyautogui.hotkey("ctrl", "v")

        SafeRunner.run(
            perform_paste,
            (),
            debug=True,
            ignore=False,
            context={"text": pyperclip.paste()},
            debug_msg=f"Pasting text: {pyperclip.paste()}",
            warn_msg=f"Failed to paste text: {pyperclip.paste()}",
            err_msg=f"Error pasting text: {pyperclip.paste()}: {{error}}",
            log_lvl=[LogLevel.INFO, LogLevel.DEBUG],
        )
        return content

    @staticmethod
    def run_command(
        command: str,
        args: Optional[List[str]],
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
        shell: bool = True,
        wait: bool = True,
        debug: bool = False,
        prefix: str = "",
    ):
        cmd = [command] + (args or [])
        process = SafeRunner.run(
            subprocess.Popen,
            (cmd,),
            {
                "env": env,
                "cwd": cwd,
                "shell": shell,
                "stdout": subprocess.PIPE,
                "stderr": subprocess.PIPE,
                "text": True,
            },
            debug_msg=f"Running command '{command}' with args {args}",
            warn_msg=f"{prefix} Failed to run command '{command}' with args {args}",
            err_msg=f"{prefix} Error running command '{command}' with args {args}",
            log_lvl=[LogLevel.INFO, LogLevel.DEBUG],
        )

        if process and wait:
            stdout, stderr = process.communicate()
            print(stdout)
            print(stderr)
