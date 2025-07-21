from typing import Dict, Literal, NotRequired, TypedDict


class ImageDict(TypedDict):
    path: str
    confidence: float


class RegionDict(TypedDict):
    x: int
    y: int
    width: int
    height: int


class WindowDict(TypedDict):
    title: NotRequired[str]
    class_name: NotRequired[str]
    process: NotRequired[str]
    allow_overlay: NotRequired[bool]
    allow_out_of_screen: NotRequired[bool]


class ROI_DebugDict(TypedDict):
    display_screenshot: NotRequired[bool]


class ROIDict(TypedDict):
    type: Literal["MoveMouse", "DetectOnly"]
    image: ImageDict
    window: NotRequired[WindowDict]
    region: NotRequired[RegionDict]
    duration: NotRequired[int]
    debug: NotRequired[ROI_DebugDict]

    returns: NotRequired[
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
    ]
