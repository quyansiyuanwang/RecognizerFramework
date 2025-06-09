import json
from collections.abc import Generator
from functools import cached_property
from typing import Any, Dict, Iterable, Optional, Self, Tuple, TypeVar, Union

from src.Typehints import NextDict
from src.Typehints.workflow import IdentifiedGlobalsDict

from ..Structure import Job
from ..Typehints import JobDict, WorkflowDict

_DEFAULT_T = TypeVar("_DEFAULT_T", bound=Any)


class WorkflowManager:
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.__current_job: Optional[str] = None
        self.iter_status: bool = True

    @cached_property
    def workflow(self) -> WorkflowDict:
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def names(self) -> Iterable[str]:
        return self.workflow["jobs"].keys()

    def jobs(self) -> Iterable[Job]:
        return [Job(name, job) for name, job in self.workflow["jobs"].items()]

    def get_globals(
        self, default: Optional[_DEFAULT_T] = None
    ) -> Union[_DEFAULT_T, IdentifiedGlobalsDict, Any]:
        return self.workflow.get("globals", default)

    def __contains__(self, name: Any) -> bool:
        return name in self.workflow["jobs"]

    def get_flow_pairs(self) -> Generator[Tuple[str, Job], None, None]:
        for name in self:
            job: Job = Job(name, self.workflow["jobs"][name])
            yield name, job
        return None

    def get_begin(self) -> str:
        return self.workflow.get("begin", "")

    def get_next(self, name: str, status: bool) -> Optional[str]:
        if name in self.workflow["jobs"]:
            job = self.workflow["jobs"][name]
            nxt: Optional[Union[str, NextDict]] = job.get("next")
            if isinstance(nxt, str):
                return nxt
            elif isinstance(nxt, dict):
                value = nxt.get("success" if status else "failure", None)
                return value if isinstance(value, str) or value is None else None
        else:
            raise ValueError(f"Job '{name}' not found in workflow.")
        return None

    def get_job(self, name: str) -> Optional[Job]:
        jobs: Dict[str, JobDict] = self.workflow["jobs"]
        if name in jobs:
            return Job(name, jobs[name])
        return None

    def __iter__(self) -> Self:
        self.__current_job = self.workflow["begin"]
        return self

    def __next__(self) -> str:
        jobs: Dict[str, JobDict] = self.workflow["jobs"]
        if self.__current_job in jobs:
            tmp_job: str = self.__current_job
            nxt = jobs[self.__current_job].get("next", None)
            if isinstance(nxt, str):
                self.__current_job = nxt
            elif nxt:
                if self.iter_status:
                    self.__current_job = nxt.get("success", None)
                else:
                    self.__current_job = nxt.get("failure", None)
            else:
                self.__current_job = None

            return tmp_job
        raise StopIteration

    def __repr__(self) -> str:
        jobs = "\n" + ", \n".join([f"{job.get('name')}: {job}" for job in self.jobs()])
        return f"WorkflowManager(path={self.path}, jobs={{ {jobs} }})"
