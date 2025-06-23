from typing import List, Literal, NotRequired, TypedDict


class KeyboardDict(TypedDict):
    # Required fields
    keys: List[str]

    # Optional fields
    duration: NotRequired[int]
    sep_time: NotRequired[int]


class MouseDict(TypedDict):
    # Required fields
    type: Literal["LClick", "RClick", "MClick", "Move", "MoveTo"]

    # Optional fields
    duration: NotRequired[int]
    x: NotRequired[int]
    y: NotRequired[int]


class TextDict(TypedDict):
    # Required fields
    text: str

    # Optional fields
    duration: NotRequired[int]


class InputDict(TypedDict):
    # Required fields
    type: Literal["Keyboard", "Mouse", "Text"]

    # Optional fields
    keyboard: NotRequired[KeyboardDict]
    mouse: NotRequired[MouseDict]
    text: NotRequired[TextDict]
