import json
from collections.abc import Generator
from functools import cached_property
from typing import Any, Dict, Iterable, List, Optional, Self, Set, Tuple, TypeVar, Union

from ..Models.globals import Globals
from ..Models.main import Job, Next, Workflow
from ..Util.util import to_indent_str
from .Exceptions.crash import OverloadError, RecursiveError, WorkflowBeginError

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
    def workflow(self) -> Workflow:
        if not self.path or not self.path.endswith(".json"):
            raise ValueError("Invalid workflow file path. Must be a .json file.")

        with open(self.path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return Workflow(**data)

    @cached_property
    def names(self) -> Iterable[str]:
        return self.workflow.jobs.keys()

    @cached_property
    def jobs(self) -> List[Job]:
        jobs: List[Job] = []
        for name in self.workflow.jobs:
            job = self.get_job(name)
            if job is not None:
                jobs.append(job)
        return jobs

    def get_globals(
        self, default: Optional[_DEFAULT_T] = None
    ) -> Union[_DEFAULT_T, Globals, Any]:
        return self.workflow.globals or default

    def __contains__(self, name: Any) -> bool:
        return name in self.workflow.jobs

    def get_flow_pairs(self) -> Generator[Tuple[str, Job], None, None]:
        for name in self.names:
            job = self.get_job(name)
            if job is not None:
                yield name, job
        return None

    def get_begin(self) -> str:
        begin = self.workflow.begin
        if not begin:
            raise WorkflowBeginError("Workflow 'begin' not found.")
        return begin

    @staticmethod
    def _merge_cpx_obj(
        parent_value: Union[Dict[str, Any], str, float, int, None, List[Any]],
        child_value: Union[Dict[str, Any], str, float, int, None, List[Any]],
    ) -> Any:
        if isinstance(parent_value, dict) and isinstance(child_value, dict):
            # Merge dictionaries recursively
            for key, value in child_value.items():
                parent_value[key] = WorkflowManager._merge_cpx_obj(
                    parent_value.get(key, {}), value
                )
            return parent_value
        else:
            # For other types, child value overrides parent value
            return child_value

    def _overload_case(self, job: Job) -> Job:
        job_name: str = job.name
        overloaded: str = job.overload
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
                    (
                        f"Overload job '{nxt}' has recursive overload. \n"
                        f"Recursive chain: {' -> '.join(chain + [nxt])}"
                    ),
                    job,
                )

        parent_job: Optional[Job] = self.get_job(overloaded)
        parent_kwargs: Optional[Job] = self.workflow.jobs.get(overloaded)
        child_kwargs: Optional[Job] = self.workflow.jobs.get(job_name, None)
        if parent_job is None or parent_kwargs is None or child_kwargs is None:
            raise OverloadError(
                f"Overload job '{overloaded}' not found in workflow or has no definition.",
                job,
            )

        pkw: Dict[str, Any] = parent_job.model_dump(exclude_unset=True)
        ckw: Dict[str, Any] = child_kwargs.model_dump(exclude_unset=True)
        for key, value in ckw.items():
            if key not in self.__OVERLOAD_IGNORE_FIELDS:
                pk = pkw.get(key, None)  # type: ignore[literal-required]
                if pk is not None and isinstance(pk, dict) and isinstance(value, dict):
                    # Merge dicts recursively
                    pkw[key] = self._merge_cpx_obj(pk, value)  # type: ignore[assignment]
                else:
                    pkw[key] = value
        overloaded_job = Job(**pkw)
        overloaded_job.name = job_name
        return overloaded_job

    def special_case(self, job: Job) -> Optional[Job]:
        if job.type == "Overload":
            return self._overload_case(job)

        return None

    def get_next(self, name: str, status: bool) -> Optional[str]:
        if name in self.workflow.jobs:
            job: Job = self.workflow.jobs[name]
            nxt: Union[str, Next] = job.next
            if isinstance(nxt, str):
                return nxt
            else:
                return nxt.success if status else nxt.failure

        return None

    def get_job(self, name: str) -> Optional[Job]:
        jobs: Dict[str, Job] = self.workflow.jobs
        if name in jobs:
            origin: Job = jobs[name]
            origin.name = name
            job: Optional[Job] = self.special_case(origin)
            while job is not None:
                origin = job
                job = self.special_case(origin)
            return origin

        return None

    def __iter__(self) -> Self:
        self.__current_job = self.get_begin()
        return self

    def __next__(self) -> Job:
        jobs: Dict[str, Job] = self.workflow.jobs
        if self.__current_job in jobs:
            tmp_job: str = self.__current_job
            nxt = jobs[self.__current_job].next
            if isinstance(nxt, str):
                self.__current_job = nxt
            elif nxt:
                if self.iter_status:
                    self.__current_job = nxt.success
                else:
                    self.__current_job = nxt.failure
            else:
                self.__current_job = None

            ret = self.get_job(tmp_job)
            if ret is not None:
                return ret
            raise StopIteration(f"Job '{tmp_job}' not found in workflow.")
        raise StopIteration

    def __repr__(self) -> str:
        jobs_repr = ",\n".join(
            f"{job.name}: {to_indent_str(job.model_dump(exclude_unset=True))}"
            for job in self.jobs
        )
        return f"WorkflowManager(path={self.path}, jobs={{\n{jobs_repr}\n}})"
