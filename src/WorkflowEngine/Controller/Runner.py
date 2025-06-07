from typing import Any, Callable, Dict, Iterable, Optional, Tuple, TypeVar

from src.Typehints.workflow import LogConfigDict

from .LogController import global_log_manager

T = TypeVar("T")
from .LogController import LogLevel


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
        log_config: Optional[LogConfigDict] = None,
    ) -> Optional[T]:
        ctx = context or {}
        if debug_msg and debug:
            global_log_manager.log(
                debug_msg.format_map({**ctx, **locals()}),
                log_lvl,
                log_config=log_config,
            )
        try:
            return fnc(*args, **kwargs)
        except Exception as e:
            if on_error:
                on_error(e)
            if ignore:
                global_log_manager.log(
                    warn_msg.format_map({**ctx, **locals(), "error": str(e)}),
                    [LogLevel.WARNING],
                    log_config=log_config,
                )
                return None
            global_log_manager.log(
                err_msg.format_map({**ctx, **locals(), "error": str(e)}),
                [LogLevel.ERROR],
                log_config=log_config,
            )
            raise RuntimeError(e) from e
