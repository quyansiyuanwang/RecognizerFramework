from typing import Optional

from ..Typehints import SystemDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("system")
class System(Base):
    def __init__(self, *, kwargs: SystemDict) -> None:
        super().__init__(kwargs=dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "System")
