from typing import Any

from ..Typehints import PositionDict
from .TypeMap import TypeMap
from .Util import repr_indent


@TypeMap.register("position")
class Position:
    def __init__(self, kwargs: PositionDict) -> None:
        self._kwargs: PositionDict = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None:
                value = tp(value)
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        return repr_indent(self, "Position", indent=indent)
