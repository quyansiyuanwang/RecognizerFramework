from typing import Any, Literal, Optional

from ...Structure import Delay
from ...Typehints.framework.frame import IdentifiedGlobalsDict
from ..Controller import SystemController


def delay(
    delay: Delay,
    mode: Literal["pre", "post"],
    globals: IdentifiedGlobalsDict,
    prefix: str = "",
    **_: Any,
) -> None:
    if mode not in {"pre", "post"}:
        assert False, f"Invalid delay mode: {mode}"

    if mode == "pre":
        pre: int = delay.get("pre", 0)
        if pre < 0:
            raise ValueError(f"Invalid delay duration: {pre} ms")
        SystemController.sleep(
            pre,
            debug=globals.get("debug", False),
            prefix=f"{prefix}ExecutorPreDelay",
        )
    else:
        post: Optional[int] = delay.get("post", None)
        if post is None:
            return
        if post < 0:
            raise ValueError(f"Invalid delay duration: {post} ms")
        SystemController.sleep(
            post,
            debug=globals.get("debug", False),
            prefix=f"{prefix}ExecutorPostDelay",
        )
