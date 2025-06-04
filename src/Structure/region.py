from typing import Any

from ..Typehints import RegionDict
from .TypeMap import TypeMap
from .Util import repr_indent


@TypeMap.register("region")
class Region:
    def __init__(self, kwargs: RegionDict) -> None:
        self._kwargs: RegionDict = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None:
                value = tp(value)
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        return repr_indent(self, "Region", indent=indent)
