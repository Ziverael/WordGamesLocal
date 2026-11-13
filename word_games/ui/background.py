from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor

from kivy.clock import Clock


_executor = ThreadPoolExecutor(max_workers=1)


def _deliver(future, on_done, on_error) -> None:
    msg = "This is a placeholder function. You should implement the logic to deliver the result of the background task to the appropriate callback functions."
    raise NotImplementedError(msg)


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
