from typing import Literal, Optional

from pydantic import BaseModel, Field


class Image(BaseModel):
    path: str = Field(..., description="图像文件路径")
    confidence: float = Field(..., description="图像识别置信度")


class Region(BaseModel):
    x: int = Field(..., description="识别区域的X坐标")
    y: int = Field(..., description="识别区域的Y坐标")
    width: int = Field(..., description="识别区域的宽度")
    height: int = Field(..., description="识别区域的高度")


class ROI(BaseModel):
    type: Literal["MoveMouse", "DetectOnly"] = Field(
        ...,
        description="ROI检测后操作类型, 可选: MoveMouse(移动鼠标), DetectOnly(仅检测)",
    )
    image: Image = Field(
        ...,
        description="ROI图像定义, 包含路径和置信度",
    )
    region: Optional[Region] = Field(
        None,
        description="ROI区域定义, 包含x, y, width, height",
    )
    duration: Optional[int] = Field(
        None,
        description="鼠标移动时间, 单位为毫秒",
    )
