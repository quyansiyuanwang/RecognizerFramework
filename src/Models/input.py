from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class Input_Mouse(BaseModel):
    type: Literal[
        "Press",
        "Release",
        "Click",
        "Move",
        "Drag",
    ] = Field(
        ...,
        description=(
            "鼠标输入类型, 可选: Press(按下), Release(释放), Click(点击), "
            "Move(移动),  Drag(拖动)"
        ),
    )
    button: Literal["LEFT", "RIGHT", "MIDDLE"] = Field(
        default="LEFT",
        description="鼠标按钮类型, 可选: LEFT(左键), RIGHT(右键), MIDDLE(中键)",
    )
    x: int = Field(default=0, description="X坐标, 像素值")
    y: int = Field(default=0, description="Y坐标, 像素值")
    duration: int = Field(default=0, ge=0, description="延时(ms), 鼠标操作时间")
    relative: bool = Field(
        default=True,
        description=(
            "是否相对当前位置移动, 默认为True, 如果为True, 则x和y表示相对偏移量"
        ),
    )
    returns: Dict[
        str,
        Literal[
            "origin_x",
            "origin_y",
            "x",
            "y",
            "duration",
            "button",
            "type",
        ],
    ] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['origin_x', 'origin_y', 'x', 'y', 'duration', 'button', 'type'], "
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )


class Input_Keyboard(BaseModel):
    type: Literal["Press", "Release", "Type"] = Field(
        ...,
        description="键盘输入类型, 可选: Press(按下), Release(释放), Type(输入)",
    )
    keys: List[str] = Field(
        default_factory=list,
        description="键盘输入的按键列表, 如['ctrl', 'v'], 支持组合键",
    )
    duration: int = Field(default=0, ge=0, description="延时(ms), 完全按下到释放的时间")
    sep_time: int = Field(
        default=0, ge=0, description="按键间隔时间(ms), 用于按键间的延时"
    )
    returns: Dict[str, Literal["keys", "type", "duration"]] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['keys', 'type', 'duration'],"
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )


class Input_Text(BaseModel):
    message: str = Field(..., description="要输入的文本内容")
    duration: int = Field(default=0, ge=0, description="延时(ms), 文本输入时间")

    returns: Dict[str, Literal["type", "message", "duration"]] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['type', 'message', 'duration']"
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )


class Input(BaseModel):
    type: Literal["Mouse", "Keyboard", "Text"] = Field(
        ...,
        description="输入类型, 可选: Mouse(鼠标输入), Keyboard(键盘输入), Text(文本输入)",
    )
    mouse: Optional[Input_Mouse] = Field(
        None, description="鼠标输入定义, 仅在type为Mouse时有效"
    )
    keyboard: Optional[Input_Keyboard] = Field(
        None, description="键盘输入定义, 仅在type为Keyboard时有效"
    )
    text: Optional[Input_Text] = Field(
        None, description="文本输入定义, 仅在type为Text时有效"
    )

    background: bool = Field(
        default=False,
        description=("是否在后台执行, 默认为False, 如果为True, 则尝试后台输入"),
    )
    focus: bool = Field(
        default=True,
        description=(
            "是否在执行输入前将窗口置于前台, 默认为True, "
            "如果为False, 则不改变当前焦点窗口"
        ),
    )
    title: str = Field(default="", description="窗口标题, 仅在后台操作时有效")
    class_name: str = Field(default="", description="窗口类名, 仅在后台操作时有效")
    process: str = Field(default="", description="进程名称, 仅在后台操作时有效")
    visible_only: bool = Field(
        default=True,
        description=("是否只查找可见窗口, 默认为True, 如果为False, 则查找所有窗口"),
    )
    exact_match: bool = Field(
        default=False,
        description=(
            "是否精确匹配窗口, 默认为False, 如果为True, 则只查找完全匹配的窗口"
        ),
    )


__all__ = [
    "Input",
    "Input_Mouse",
    "Input_Keyboard",
    "Input_Text",
]
