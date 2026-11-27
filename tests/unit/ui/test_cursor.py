from pathlib import Path

import pytest
from kivy.metrics import dp
from kivy.uix.widget import Widget

from word_games.ui import cursor as _cursor
from word_games.ui.cursor import CursorShape
from word_games.ui.palette import ActivePalette
from word_games.ui.preferences import ActivePreferences
from word_games.ui.theme import ThemeName


pytestmark = pytest.mark.atomic


class FakeWindow:
    def __init__(self) -> None:
        self.canvas = Widget().canvas
        self.show_cursor = True
        self.handlers: dict[str, object] = {}
        self.system_cursor = ""

    def bind(self, **handlers: object) -> None:
        self.handlers.update(handlers)

    def set_system_cursor(self, cursor_name: str) -> bool:
        self.system_cursor = cursor_name
        return True


@pytest.fixture
def window() -> FakeWindow:
    return FakeWindow()


@pytest.fixture
def palette() -> ActivePalette:
    return ActivePalette()


@pytest.fixture
def preferences() -> ActivePreferences:
    return ActivePreferences()


@pytest.fixture
def cursor(window, palette, preferences) -> _cursor.ThemedCursor:
    return _cursor.ThemedCursor(window, palette, preferences)


def test_system_cursor_is_hidden_inside_the_window(window, cursor):
    # then
    assert window.show_cursor is False


def test_cursor_follows_the_mouse(window, cursor):
    # when
    window.handlers["mouse_pos"](window, (120, 80))

    # then
    assert cursor._position.xy == (120, 80)


@pytest.mark.parametrize("shape", list(CursorShape))
def test_shown_shape_uses_its_image_for_the_current_theme(
    cursor, palette, shape
):
    # when
    cursor.show(shape)

    # then
    assert cursor._image.source == _cursor.locate_cursor(
        shape, palette.theme_name
    )


@pytest.mark.parametrize("theme_name", list(ThemeName))
def test_cursor_image_follows_the_applied_theme(cursor, palette, theme_name):
    # when
    palette.apply_theme(theme_name)

    # then
    assert cursor._image.source == _cursor.locate_cursor(
        CursorShape.arrow, theme_name
    )


def test_hotspot_lands_on_the_mouse_position(cursor):
    # given
    hotspot = _cursor.HOTSPOTS[CursorShape.text]

    # when
    cursor.show(CursorShape.text)
    left, bottom = cursor._image.pos
    _, height = cursor._image.size

    # then
    assert (left + dp(hotspot.x), bottom + height - dp(hotspot.y)) == (0, 0)


@pytest.mark.parametrize("theme_name", list(ThemeName))
def test_every_shape_has_an_image_in_every_theme(theme_name):
    # when
    missing = [
        shape
        for shape in CursorShape
        if not Path(_cursor.locate_cursor(shape, theme_name)).is_file()
    ]

    # then
    assert missing == []


def test_system_cursor_preference_shows_the_system_cursor(
    window, cursor, preferences
):
    # when
    preferences.use_system_cursor = True

    # then
    assert (window.show_cursor, cursor._visibility.a) == (True, 0)


@pytest.mark.parametrize("shape", list(CursorShape))
def test_system_cursor_still_changes_shape_on_hover(
    window, cursor, preferences, shape
):
    # given
    preferences.use_system_cursor = True

    # when
    cursor.show(shape)

    # then
    assert window.system_cursor == _cursor.SYSTEM_CURSORS[shape]


def test_turning_the_preference_off_brings_back_the_themed_cursor(
    window, cursor, preferences
):
    # given
    preferences.use_system_cursor = True

    # when
    preferences.use_system_cursor = False

    # then
    assert (window.show_cursor, cursor._visibility.a) == (False, 1)


def test_cursor_is_hidden_when_the_mouse_leaves_the_window(window, cursor):
    # when
    window.handlers["on_cursor_leave"](window)

    # then
    assert cursor._visibility.a == 0


def test_cursor_reappears_when_the_mouse_comes_back(window, cursor):
    # given
    window.handlers["on_cursor_leave"](window)

    # when
    window.handlers["on_cursor_enter"](window)

    # then
    assert cursor._visibility.a == 1


def test_coming_back_keeps_the_themed_cursor_hidden_for_system_cursor(
    window, cursor, preferences
):
    # given
    preferences.use_system_cursor = True
    window.handlers["on_cursor_leave"](window)

    # when
    window.handlers["on_cursor_enter"](window)

    # then
    assert (window.show_cursor, cursor._visibility.a) == (True, 0)
