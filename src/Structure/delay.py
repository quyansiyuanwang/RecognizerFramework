from typing import Optional

from ..Typehints import DelayDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("delay")
class Delay(Base):
    def __init__(self, kwargs: DelayDict) -> None:
        super().__init__(dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Delay")
