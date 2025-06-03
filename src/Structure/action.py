from typing import Any, Optional
from ..Typehints import ActionDict
from .TypeMap import TypeMap


@TypeMap.register("action")
class Action:
    def __init__(self, kwargs: ActionDict) -> None:
        self._kwargs: ActionDict = kwargs

        for key, value in self._kwargs.items():
            tp = TypeMap.get(key=key)
            if tp is not None:
                value = tp(value)
            setattr(self, key, value)

    def __getattr__(self, item: str) -> Optional[Any]:
        if item in self._kwargs:
            return self._kwargs.get(item)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'"
        )

    def __repr__(self, indent: int = 0) -> str:
        string: str = "<Action(\n"
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
