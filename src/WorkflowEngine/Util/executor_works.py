from typing import Any, Dict, Literal, Mapping, Optional, TypeVar, Union

from pydantic import BaseModel

from ...Models.globals import Globals
from ...Models.main import Delay
from ..Controller import SystemController


def delay(
    delay: Delay,
    mode: Literal["pre", "post"],
    globals: Globals,
    prefix: str = "",
    **_: Any,
) -> None:
    if mode not in {"pre", "post"}:
        assert False, f"Invalid delay mode: {mode}"

    if mode == "pre":
        pre: int = delay.pre
        if pre < 0:
            raise ValueError(f"Invalid delay duration: {pre} ms")
        SystemController.sleep(
            pre,
            debug=globals.debug,
            prefix=f"{prefix}ExecutorPreDelay",
        )
    else:
        post: int = delay.post
        if post < 0:
            raise ValueError(f"Invalid delay duration: {post} ms")
        SystemController.sleep(
            post,
            debug=globals.debug,
            prefix=f"{prefix}ExecutorPostDelay",
        )


def update(
    model: Union[Mapping[str, Any], BaseModel], kwargs: Dict[str, Any], **aft_kws: Any
) -> None:
    kwargs.update(aft_kws)
    for key, value in kwargs.items():
        if hasattr(model, key):
            setattr(model, key, value)
        else:
            raise AttributeError(
                f"Model {model.__class__.__name__} has no attribute '{key}'"
            )


_T = TypeVar("_T")


def get(model: Optional[BaseModel], key: str, default: _T) -> _T:
    return getattr(model, key, default) if model else default
