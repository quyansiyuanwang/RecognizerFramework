from typing import Literal, Optional, TypedDict


class ImageDict(TypedDict):
    path: str
    confidence: float


class RegionDict(TypedDict):
    x: int
    y: int
    width: int
    height: int


class ROIDict(TypedDict):
    type: Literal["MoveMouse", "DetectOnly"]
    image: ImageDict
    region: Optional[RegionDict]
    duration: Optional[int]
