from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class Input_Mouse(BaseModel):
    type: Literal["LClick", "RClick", "MClick", "Move", "MoveTo"] = Field(
        ...,
        description="鼠标输入类型, 可选: LClick(左键点击), RClick(右键点击), MClick(中键点击), Move(移动鼠标), MoveTo(移动到指定位置)",
    )
    x: Optional[int] = Field(None, description="X坐标, 像素值")
    y: Optional[int] = Field(None, description="Y坐标, 像素值")
    duration: Optional[int] = Field(0, ge=0, description="延时(ms), 鼠标操作时间")


class Input_Keyboard(BaseModel):
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
