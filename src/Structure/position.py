from typing import Any, Literal

from ..Typehints import PositionDict
from .TypeMap import TypeMap


@TypeMap.register("position")
class Position:
    def __init__(self, kwargs: PositionDict) -> None:
        self.type: Literal["absolute", "relative"] = kwargs.get("type", "absolute")
        self.x: int = kwargs.get("x", 0)
        self.y: int = kwargs.get("y", 0)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        string: str = "<Position(\n"
        for key, value in self.__dict__.items():
            if value is None:
                continue
            is_indentable: bool = not isinstance(
                value, (str, int, float, bool, dict, set, list, tuple)
            )
            representation: str = (
                value.__repr__(indent + 4) if is_indentable else value.__repr__()
            )
            string += f"{' ' * (indent + 4)}{key}={representation},\n"
        string = string.rstrip(",\n") + "\n" + " " * indent + ")>"
        return string
