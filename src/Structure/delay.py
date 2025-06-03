from typing import Any

from ..Typehints import DelayDict
from .TypeMap import TypeMap


@TypeMap.register("delay")
class Delay:
    def __init__(self, kwargs: DelayDict) -> None:
        self.pre = kwargs.get("pre", 0)
        self.cur = kwargs.get("cur", 0)
        self.post = kwargs.get("post", 0)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        string = "<Delay(\n"
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
