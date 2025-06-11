import json
from collections.abc import Generator
from functools import cached_property
from typing import Any, Dict, Iterable, List, Optional, Self, Set, Tuple, TypeVar, Union

from src.Typehints import IdentifiedGlobalsDict, JobDict, NextDict, WorkflowDict
from src.WorkflowEngine.exceptions import OverloadError, RecursiveError

from ..Structure import Job

_DEFAULT_T = TypeVar("_DEFAULT_T", bound=Any)


class WorkflowManager:
    __OVERLOAD_IGNORE_FIELDS: Set[str] = {
        "type",
        "overload",
    }
    __RelativedOverloadMap: Dict[str, str] = {}

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
        for name in self.names():
            job: Job = Job(name, self.workflow["jobs"][name])
            yield name, job
        return None

    def get_begin(self) -> str:
        return self.workflow.get("begin", "")

    def _overload_case(self, job: Job) -> Job:
        job_name: str = job.get("name", "")
        overloaded: str = job.get("overload", "")
        # Check recursive
        self.__RelativedOverloadMap[job_name] = overloaded
        cur = job_name
        chain: List[str] = []
        while cur in self.__RelativedOverloadMap:
            cur = self.__RelativedOverloadMap[cur]
            chain.append(cur)
            if cur == job_name:
                nxt = self.__RelativedOverloadMap[cur]
                raise RecursiveError(
                    job,
                    (
                        f"Overload job '{nxt}' has recursive overload. \n"
                        f"Recursive chain: {' -> '.join(chain + [nxt])}"
                    ),
                )

        parent_job: Optional[Job] = self.get_job(overloaded)
        parent_kwargs: Optional[JobDict] = self.workflow["jobs"].get(overloaded)
        child_kwargs: Optional[JobDict] = self.workflow["jobs"].get(job_name, None)
        if parent_job is None or parent_kwargs is None or child_kwargs is None:
            raise OverloadError(
                job,
                f"Overload job '{overloaded}' not found in workflow or has no definition.",
            )

        parent_kwargs.update({"name": job_name})
        for key in child_kwargs:
            if key not in self.__OVERLOAD_IGNORE_FIELDS:
                parent_kwargs[key] = child_kwargs[key]  # type: ignore[literal-required]
        return Job(job_name, parent_kwargs)

    def special_case(self, job: Job) -> Optional[Job]:
        if job["type"] == "Overload":
            return self._overload_case(job)

        return None

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
            origin: Job = Job(name, jobs[name])
            job: Optional[Job] = self.special_case(origin)
            while job is not None:
                origin = job
                job = self.special_case(origin)
            return origin

        return None

    def __iter__(self) -> Self:
        self.__current_job = self.workflow["begin"]
        return self

    def __next__(self) -> Job:
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

            ret = self.get_job(tmp_job)
            if ret is not None:
                return ret
            raise StopIteration(f"Job '{tmp_job}' not found in workflow.")
        raise StopIteration

    def __repr__(self) -> str:
        jobs = "\n" + ", \n".join([f"{job.get('name')}: {job}" for job in self.jobs()])
        return f"WorkflowManager(path={self.path}, jobs={{ {jobs} }})"
