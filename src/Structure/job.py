from typing import Any

from ..Typehints import JobDict
from .TypeMap import TypeMap


@TypeMap.register("job")
class Job:
    def __init__(self, kwargs: JobDict) -> None:
        self._kwargs: JobDict = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None:
                value = tp(value)
            setattr(self, key, value)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def __repr__(self, indent: int = 0) -> str:
        string: str = "<Job(\n"
        for key, value in self.__dict__.items():
            if value is None or key.startswith("_"):
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
