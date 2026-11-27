import pytest
from kivy.uix.widget import Widget
from pytest_mock import MockerFixture

from word_games.ui import hover as _hover
from word_games.ui.cursor import CursorShape


pytestmark = pytest.mark.atomic


class HoverableWidget(_hover.HoverBehavior, Widget):
    pass


class TextLikeWidget(_hover.HoverBehavior, Widget):
    cursor_shape = CursorShape.text


class FakeWindow:
    def __init__(self) -> None:
        self.move_pointer = None

    def bind(self, mouse_pos) -> None:
        self.move_pointer = mouse_pos


class FakeCursor:
    def __init__(self) -> None:
        self.shape: CursorShape | None = None

    def show(self, shape: CursorShape) -> None:
        self.shape = shape


@pytest.fixture
def window() -> FakeWindow:
    return FakeWindow()


@pytest.fixture
def cursor() -> FakeCursor:
    return FakeCursor()


@pytest.fixture
def tracker(window, cursor) -> _hover.PointerTracker:
    return _hover.PointerTracker(window, cursor)


@pytest.fixture
def widget(window, mocker: MockerFixture) -> HoverableWidget:
    widget = HoverableWidget(pos=(100, 100), size=(50, 50))
    mocker.patch.object(widget, "get_root_window", return_value=window)
    return widget


@pytest.mark.parametrize(
    ("position", "expected"),
    [
        pytest.param((120, 120), (True, CursorShape.pointer), id="inside"),
        pytest.param((10, 10), (False, CursorShape.arrow), id="outside"),
    ],
)
def test_pointer_move_sets_hover_and_cursor(
    window, cursor, tracker, widget, position, expected
):
    # when
    window.move_pointer(window, position)

    # then
    assert (widget.hovered, cursor.shape) == expected


def test_widget_outside_any_window_is_never_hovered(window, tracker):
    # given
    detached = HoverableWidget(pos=(100, 100), size=(50, 50))

    # when
    window.move_pointer(window, (120, 120))

    # then
    assert detached.hovered is False


def test_widget_clipped_by_its_container_is_not_hovered(
    window, tracker, widget
):
    # given
    container = Widget(pos=(0, 0), size=(110, 110))
    container.add_widget(widget)

    # when
    window.move_pointer(window, (140, 140))

    # then
    assert widget.hovered is False


def test_forgetting_hovered_widgets_restores_the_cursor(
    window, cursor, tracker, widget
):
    # given
    window.move_pointer(window, (120, 120))

    # when
    tracker.forget_hovered_widgets()

    # then
    assert (widget.hovered, cursor.shape) == (False, CursorShape.arrow)


def test_text_field_inside_a_clickable_widget_shows_the_text_cursor(
    window, cursor, tracker, widget, mocker: MockerFixture
):
    # given
    text_field = TextLikeWidget(pos=(110, 110), size=(30, 30))
    mocker.patch.object(text_field, "get_root_window", return_value=window)

    # when
    window.move_pointer(window, (120, 120))

    # then
    assert cursor.shape == CursorShape.text
