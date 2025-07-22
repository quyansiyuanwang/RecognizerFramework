from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field


class ROI_Image(BaseModel):
    path: str = Field(..., description="图像文件路径")
    confidence: float = Field(..., description="图像识别置信度")


class ROI_Region(BaseModel):
    x: int = Field(default=..., description="识别区域的X坐标")
    y: int = Field(default=..., description="识别区域的Y坐标")
    width: int = Field(default=..., description="识别区域的宽度")
    height: int = Field(default=..., description="识别区域的高度")


class ROI_Window(BaseModel):
    title: str = Field(default="", description="窗口标题, 可选")
    class_name: str = Field(default="", description="窗口类名, 可选")
    process: str = Field(default="", description="进程名称, 可选")
    allow_overlay: bool = Field(default=True, description="是否允许其他窗口覆盖, 可选")
    allow_out_of_screen: bool = Field(
        default=False, description="是否允许截屏区域超出屏幕, 可选"
    )


class ROI_Debug(BaseModel):
    display_screenshot: bool = Field(
        default=False,
        description="是否显示截图, 默认为False",
    )


class ROI(BaseModel):
    type: Literal["MoveMouse", "DetectOnly"] = Field(
        default=...,
        description="ROI检测后操作类型, 可选: MoveMouse(移动鼠标), DetectOnly(仅检测)",
    )
    image: ROI_Image = Field(
        default=...,
        description="ROI图像定义, 包含路径和置信度",
    )
    window: Optional[ROI_Window] = Field(
        default=None,
        description="ROI窗口定义, 包含标题, 类名和进程名称, 注意: 某些窗口可能反截屏, 而且可能存在截图兼容性问题",
    )
    region: Optional[ROI_Region] = Field(
        default=None,
        description="ROI区域定义, 包含x, y, width, height",
    )
    duration: int = Field(
        default=0,
        description="鼠标移动时间, 单位为毫秒",
    )
    debug: ROI_Debug = Field(
        default_factory=ROI_Debug,
        description="调试参数",
    )
    returns: Dict[
        str,
        Literal[
            "center_x",
            "center_y",
            "confidence",
            "left",
            "top",
            "right",
            "bottom",
            "width",
            "height",
            "template_height",
            "template_width",
        ],
    ] = Field(
        default_factory=dict,
        description=(
            "返回值变量字典, 包含['center_x', 'center_y', 'confidence', 'left', 'top', 'right', 'bottom', 'width', 'height', 'template_height', 'template_width'], "
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )
