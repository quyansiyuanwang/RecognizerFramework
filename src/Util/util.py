from collections.abc import Mapping
from typing import Any, Dict, List, Union

from ..Typehints.basic import BaseObject


def kwargs_getter(kwargs: Mapping[str, Any], key: str, tp: type) -> Any | None:
    return tp(kwargs.get(key, {})) if kwargs.get(key) else None


def to_indent_str(obj: Union[Dict[str, Any], BaseObject], level: int = 0) -> str:
    pad = "  " * level
    if isinstance(obj, dict):
        items: List[str] = []
        for k, v in obj.items():
            items.append(f"{pad}  {k}: {to_indent_str(v, level + 1)}")
        return "{\n" + ",\n".join(items) + f"\n{pad}}}"
    return repr(obj)
