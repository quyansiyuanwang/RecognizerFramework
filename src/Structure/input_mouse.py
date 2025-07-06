from typing import Optional

from ..Typehints import MouseDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("input::mouse")
class Mouse(Base):
    def __init__(self, *, kwargs: MouseDict, _prefix: str = "") -> None:
        super().__init__(kwargs=dict(kwargs), _prefix=_prefix)

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Mouse")
