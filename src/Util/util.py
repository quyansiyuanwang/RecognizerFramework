from collections.abc import Mapping
from typing import Any


def kwargs_getter(kwargs: Mapping[str, Any], key: str, tp: type) -> Any | None:
    return tp(kwargs.get(key, {})) if kwargs.get(key) else None
