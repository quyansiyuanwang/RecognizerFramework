from typing import Optional

from ..Typehints import LimitsDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("limits")
class Limits(Base):
    def __init__(self, kwargs: LimitsDict) -> None:
        super().__init__(dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Limit")
