from typing import Any

from ..Typehints import ActionDict
from .TypeMap import TypeMap
from .Util import repr_indent


@TypeMap.register("action")
class Action:
    def __init__(self, kwargs: ActionDict) -> None:
        self._kwargs: ActionDict = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None:
                value = tp(value)
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        return repr_indent(self, "Action", indent=indent)
