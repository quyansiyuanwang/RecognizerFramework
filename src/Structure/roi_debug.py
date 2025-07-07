from typing import Optional

from ..Typehints import ROI_DebugDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("roi::debug")
class ROI_Debug(Base):
    def __init__(self, *, kwargs: ROI_DebugDict, _prefix: str = "") -> None:
        super().__init__(kwargs=dict(kwargs), _prefix=_prefix)

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "ROI_Debug")
