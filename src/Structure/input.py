from typing import Optional

from ..Typehints import InputDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("input")
class Input(Base):
    def __init__(self, *, kwargs: InputDict) -> None:
        super().__init__(kwargs=dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Input")
