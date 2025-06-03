from typing import Any

from ..Typehints import ImageDict
from .TypeMap import TypeMap


@TypeMap.register("image")
class Image:
    def __init__(self, kwargs: ImageDict):
        self.path: str = kwargs["path"]
        self.confidence: float = kwargs["confidence"]

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        string = "<Image(\n"
        for key, value in self.__dict__.items():
            if value is None:
                continue
            is_indentable: bool = not isinstance(
                value, (str, int, float, bool, dict, set, list, tuple)
            )
            representation: str = (
                value.__repr__(indent + 4) if is_indentable else f"{value}"
            )
            string += f"{' ' * (indent + 4)}{key}={representation},\n"
        string = string.rstrip(",\n") + "\n" + " " * indent + ")>"
        return string
