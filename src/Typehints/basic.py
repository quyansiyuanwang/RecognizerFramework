from typing import Tuple, Type, TypeAlias, Union

Digit: TypeAlias = Union[int, float]
BaseObject: TypeAlias = Union[str, int, float, bool, None]
BaseObjectTuple: Tuple[Type[str], Type[int], Type[float], Type[bool], None] = (
    str,
    int,
    float,
    bool,
    None,
)
