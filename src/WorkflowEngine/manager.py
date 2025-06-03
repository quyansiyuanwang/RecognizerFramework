import json
from functools import cached_property
from typing import Dict, Iterable, Optional, Self, Tuple

from ..Structure import Job
from ..Typehints import JobDict, WorkflowDict


class WorkflowManager:
    def __init__(self, path: str) -> None:
        self.path = path
        self.__current_job: Optional[str] = None

    @cached_property
    def workflow(self) -> WorkflowDict:
        with open(self.path, "r") as f:
            return json.load(f)

    def names(self) -> Iterable[str]:
        return self.workflow["jobs"].keys()

    def jobs(self) -> Iterable[Job]:
        return [Job(job) for job in self.workflow["jobs"].values()]

    def items(self) -> Iterable[Tuple[str, Job]]:
        return ((name, Job(job)) for name, job in self.workflow["jobs"].items())

    def __iter__(self) -> Self:
        self.__current_job = self.workflow["begin"]
        return self

    def __next__(self) -> str:
        jobs: Dict[str, JobDict] = self.workflow["jobs"]
        if self.__current_job in jobs:
            tmp_job: str = self.__current_job
            self.__current_job = jobs[self.__current_job].get("next")
            return tmp_job
        raise StopIteration
