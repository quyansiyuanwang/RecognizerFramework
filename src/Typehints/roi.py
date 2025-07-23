from typing import TypedDict

from PIL.Image import Image as PILImage


## ROIExecutor Type Hints
class WindowLocationDict(TypedDict):
    left: int
    top: int
    mat: PILImage
