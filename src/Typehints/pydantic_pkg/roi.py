from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field


class Image(BaseModel):
    path: str = Field(..., description="图像文件路径")
    confidence: float = Field(..., description="图像识别置信度")


class Region(BaseModel):
    x: int = Field(..., description="识别区域的X坐标")
    y: int = Field(..., description="识别区域的Y坐标")
    width: int = Field(..., description="识别区域的宽度")
    height: int = Field(..., description="识别区域的高度")


class Window(BaseModel):
    title: Optional[str] = Field(None, description="窗口标题, 可选")
    class_name: Optional[str] = Field(None, description="窗口类名, 可选")
    process: Optional[str] = Field(None, description="进程名称, 可选")
    allow_overlay: Optional[bool] = Field(
        True, description="是否允许其他窗口覆盖, 可选"
    )
    allow_out_of_screen: Optional[bool] = Field(
        False, description="是否允许截屏区域超出屏幕, 可选"
    )


class ROI_Debug(BaseModel):
    display_screenshot: Optional[bool] = Field(
        False,
        description="是否显示截图, 默认为False",
    )


class ROI(BaseModel):
    type: Literal["MoveMouse", "DetectOnly"] = Field(
        ...,
        description="ROI检测后操作类型, 可选: MoveMouse(移动鼠标), DetectOnly(仅检测)",
    )
    image: Image = Field(
        ...,
        description="ROI图像定义, 包含路径和置信度",
    )
    window: Optional[Window] = Field(
        None,
        description="ROI窗口定义, 包含标题, 类名和进程名称, 注意: 某些窗口可能反截屏, 而且可能存在截图兼容性问题",
    )
    region: Optional[Region] = Field(
        None,
        description="ROI区域定义, 包含x, y, width, height",
    )
    duration: Optional[int] = Field(
        None,
        description="鼠标移动时间, 单位为毫秒",
    )
    debug: Optional[ROI_Debug] = Field(
        None,
        description="调试参数",
    )
    returns: Optional[
        Dict[
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
        ]
    ] = Field(
        None,
        description=(
            "返回值变量字典, 包含['center_x', 'center_y', 'confidence', 'left', 'top', 'right', 'bottom', 'width', 'height', 'template_height', 'template_width'], "
            "以键为变量, 值指定返回参数, 可在其他Job中使用use指定该job返回的参数"
        ),
    )
