from typing import Any

from ..Typehints import ImageDict
from .TypeMap import TypeMap
from .Util import repr_indent


@TypeMap.register("image")
class Image:
    def __init__(self, kwargs: ImageDict):
        self._kwargs: ImageDict = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None:
                value = tp(value)
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        return repr_indent(self, "Image", indent=indent)
