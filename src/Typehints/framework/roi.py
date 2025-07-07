from typing import Literal, NotRequired, TypedDict


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


class ROI_DebugDict(TypedDict):
    display_screenshot: NotRequired[bool]


class ROIDict(TypedDict):
    type: Literal["MoveMouse", "DetectOnly"]
    image: ImageDict
    window: NotRequired[WindowDict]
    region: NotRequired[RegionDict]
    duration: NotRequired[int]
    debug: NotRequired[ROI_DebugDict]
