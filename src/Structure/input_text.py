from typing import Optional

from ..Typehints import TextDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("input::text")
class Text(Base):
    def __init__(self, *, kwargs: TextDict, _prefix: str = "") -> None:
        super().__init__(kwargs=dict(kwargs), _prefix=_prefix)

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Text")
