from typing import Any, Dict, Optional

from .TypeMap import TypeMap
from .Util import repr_indent


class Base:
    def __init__(self, *, kwargs: Dict[str, Any]) -> None:
        self._kwargs: Dict[str, Any] = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None and isinstance(value, dict):
                value = tp(kwargs=value)
            setattr(self, key, value)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def set(self, key: str, value: Any) -> None:
        setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return repr_indent(self, _name or self.__class__.__name__, indent=indent)
