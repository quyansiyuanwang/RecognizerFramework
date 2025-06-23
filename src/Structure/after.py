from typing import Optional

from ..Typehints import AfterDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("after")
class After(Base):
    def __init__(self, *, kwargs: AfterDict) -> None:
        super().__init__(kwargs=dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "After")
