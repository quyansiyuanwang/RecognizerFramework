from typing import Optional

from ..Typehints import JobDict
from .Base import Base
from .TypeMap import TypeMap


@TypeMap.register("job")
class Job(Base):
    def __init__(self, name: str, *, kwargs: JobDict, _prefix: str = "") -> None:
        kwargs.update({"name": name})  # NOTE: This is the job name, 特殊处理
        super().__init__(kwargs=dict(kwargs), _prefix=_prefix)

    def __repr__(self, indent: int = 0, _name: Optional[str] = None) -> str:
        return super().__repr__(indent, "Job")
