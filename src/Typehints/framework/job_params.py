from typing import List, NotRequired, Optional, TypedDict


class DelayDict(TypedDict):
    pre: NotRequired[int]
    post: NotRequired[int]


class LimitsDict(TypedDict):
    maxCount: NotRequired[int]
    maxFailure: NotRequired[int]
    maxSuccess: NotRequired[int]
    exit: NotRequired[Optional[str]]


class NextDict(TypedDict):
    success: NotRequired[str]
    failure: NotRequired[str]


class AfterDict(TypedDict):
    success: NotRequired[List[str]]
    failure: NotRequired[List[str]]
    always: NotRequired[List[str]]
    ignore_errors: NotRequired[bool]


class UseDict(TypedDict): ...


class BeforeDict(TypedDict):
    tasks: List[str]
    ignore_errors: NotRequired[bool]
