import os
import sys
from typing import Optional


def get_current_dir(file: Optional[str] = None) -> str:
    """Get the path of the executable or script."""
    path = (
        os.path.dirname(sys.executable)
        if getattr(sys, "frozen", False)
        else os.path.dirname(os.path.abspath(__file__))
    )
    if file:
        return os.path.join(path, file)
    return path


def is_relative_path(path: str) -> bool:
    """Check if a path is relative."""
    return not os.path.isabs(path)


def is_absolute_path(path: str) -> bool:
    """Check if a path is absolute."""
    return os.path.isabs(path)
