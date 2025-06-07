import time

from .Runner import SafeRunner


class SystemController:
    @staticmethod
    def sleep(ms: float, debug: bool = True, ignore: bool = False) -> None:
        if ms < 0:
            if ignore:
                return
            raise ValueError("Sleep duration must be non-negative")

        SafeRunner.run(
            time.sleep,
            (ms / 1000,),
            debug=debug,
            ignore=ignore,
            # logger
            context={"ms": ms},
            debug_msg="Sleeping for {ms} ms",
            warn_msg="Failed to sleep for {ms} ms",
            err_msg="Error sleeping for {ms} ms: {error}",
        )
