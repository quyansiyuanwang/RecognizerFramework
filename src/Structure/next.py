from typing import Optional, Union

from ..Typehints import NextDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("next")
class Next(Base):
    def __init__(self, *, kwargs: Union[str, NextDict], _prefix: str = "") -> None:
        if isinstance(kwargs, str):
            kwargs = {"success": kwargs}
        super().__init__(kwargs=dict(kwargs), _prefix=_prefix)

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Next")
