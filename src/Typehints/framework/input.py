from typing import List, Literal, NotRequired, TypedDict


class KeyboardDict(TypedDict):
    # Required fields
    type: Literal["Press", "Release", "Type"]
    keys: List[str]

    # Optional fields
    duration: NotRequired[int]
    sep_time: NotRequired[int]


class MouseDict(TypedDict):
    # Required fields
    type: Literal[
        "Press",
        "Release",
        "Click",
        "Move",
        "Drag",
    ]
    button: Literal["LEFT", "RIGHT", "MIDDLE"]

    # Optional fields
    duration: NotRequired[int]
    relative: NotRequired[bool]
    x: NotRequired[int]
    y: NotRequired[int]


class TextDict(TypedDict):
    # Required fields
    message: str

    # Optional fields
    duration: NotRequired[int]


class InputDict(TypedDict):
    # Required fields
    type: Literal["Keyboard", "Mouse", "Text"]

    # Optional fields
    keyboard: NotRequired[KeyboardDict]
    mouse: NotRequired[MouseDict]
    text: NotRequired[TextDict]
