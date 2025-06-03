from ..Typehints import RegionDict
from .TypeMap import TypeMap


@TypeMap.register("region")
class Region:
    def __init__(self, kwargs: RegionDict) -> None:
        self.x: int = kwargs.get("x", 0)
        self.y: int = kwargs.get("y", 0)
        self.width: int = kwargs.get("width", 0)
        self.height: int = kwargs.get("height", 0)

    def __repr__(self, indent: int = 0) -> str:
        string: str = "<Region(\n"
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
