from typing import List, Literal, Optional

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
    button: Optional[Literal["LEFT", "RIGHT", "MIDDLE"]] = Field(
        None, description="鼠标按钮类型, 可选: LEFT(左键), RIGHT(右键), MIDDLE(中键)"
    )
    x: Optional[int] = Field(None, description="X坐标, 像素值")
    y: Optional[int] = Field(None, description="Y坐标, 像素值")
    duration: Optional[int] = Field(0, ge=0, description="延时(ms), 鼠标操作时间")
    relative: Optional[bool] = Field(
        False,
        description=(
            "是否相对当前位置移动, 默认为False, 如果为True, 则x和y表示相对偏移量"
        ),
    )


class Input_Keyboard(BaseModel):
    type: Literal["Press", "Release", "Type"] = Field(
        ..., description="键盘输入类型, 可选: Press(按下), Release(释放), Type(输入)"
    )
    keys: List[str] = Field(
        ...,
        description="键盘输入的按键列表, 如['ctrl', 'v'], 支持组合键",
    )
    duration: Optional[int] = Field(
        0, ge=0, description="延时(ms), 完全按下到释放的时间"
    )
    sep_time: Optional[int] = Field(
        0, ge=0, description="按键间隔时间(ms), 用于按键间的延时"
    )


class Input_Text(BaseModel):
    message: str = Field(..., description="要输入的文本内容")
    duration: Optional[int] = Field(0, ge=0, description="延时(ms), 文本输入时间")


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
