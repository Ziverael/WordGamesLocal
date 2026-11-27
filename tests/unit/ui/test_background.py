from concurrent.futures import Future

import pytest
from pytest_mock import MockerFixture

from word_games.ui import background as _background


pytestmark = pytest.mark.atomic


def test_result_is_delivered_to_on_done(mocker: MockerFixture):
    # given
    future: Future[str] = Future()
    future.set_result("saved")
    on_done, on_error = mocker.Mock(), mocker.Mock()

    # when
    _background._deliver(future, on_done, on_error)

    # then
    assert (on_done.call_args_list, on_error.called) == (
        [mocker.call("saved")],
        False,
    )


def test_exception_is_delivered_to_on_error(mocker: MockerFixture):
    # given
    error = OSError("read-only folder")
    future: Future[str] = Future()
    future.set_exception(error)
    on_done, on_error = mocker.Mock(), mocker.Mock()

    # when
    _background._deliver(future, on_done, on_error)

    # then
    assert (on_done.called, on_error.call_args_list) == (
        False,
        [mocker.call(error)],
    )
