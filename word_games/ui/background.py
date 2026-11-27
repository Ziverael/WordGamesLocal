from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor

from kivy.clock import Clock


_executor = ThreadPoolExecutor(max_workers=1)


def _deliver[T](
    future: Future[T],
    on_done: Callable[[T], None],
    on_error: Callable[[Exception], None],
) -> None:
    error = future.exception()
    if error is None:
        on_done(future.result())
    elif isinstance(error, Exception):
        on_error(error)
    else:
        raise error


def run_in_background[T](
    task: Callable[[], T],
    on_done: Callable[[T], None],
    on_error: Callable[[Exception], None],
) -> None:
    future = _executor.submit(task)
    future.add_done_callback(
        lambda f: Clock.schedule_once(
            lambda _dt: _deliver(f, on_done, on_error)
        )
    )
