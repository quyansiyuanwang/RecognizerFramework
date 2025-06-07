from typing import Any, Callable, Dict, Iterable, Optional, Tuple, TypeVar

T = TypeVar("T")
from .LogController import Logger, LogLevel


class SafeRunner:
    @staticmethod
    def run(
        fnc: Callable[..., T],
        args: Tuple[Any, ...] = (),
        kwargs: Dict[str, Any] = {},
        *,
        log_lvl: Iterable[LogLevel] = [LogLevel.DEBUG],
        debug: bool = True,
        ignore: bool = False,
        debug_msg: str = "",
        warn_msg: str = "",
        err_msg: str = "",
        on_error: Optional[Callable[[Exception], None]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[T]:
        ctx = context or {}
        if debug_msg and debug:
            Logger.log(debug_msg.format_map({**ctx, **locals()}), log_lvl)
        try:
            return fnc(*args, **kwargs)
        except Exception as e:
            if on_error:
                on_error(e)
            if ignore:
                Logger.warning(
                    warn_msg.format_map({**ctx, **locals(), "error": str(e)}),
                )
                return None
            Logger.error(
                err_msg.format_map({**ctx, **locals(), "error": str(e)}),
            )
            raise RuntimeError(e) from e
