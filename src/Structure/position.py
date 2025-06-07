from typing import Optional

from ..Typehints import PositionDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("position")
class Position(Base):
    def __init__(self, kwargs: PositionDict) -> None:
        super().__init__(dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Position")
