from typing import Optional

from ..Typehints import JobDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("job")
class Job(Base):
    def __init__(self, kwargs: JobDict) -> None:
        super().__init__(dict(kwargs))

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Job")
