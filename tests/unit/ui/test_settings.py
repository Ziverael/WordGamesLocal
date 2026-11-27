from collections.abc import Iterator
from unittest.mock import Mock

import pytest
from pytest_mock import MockerFixture

from word_games.ui.palette import palette
from word_games.ui.preferences import preferences
from word_games.ui.screens import settings as _settings
from word_games.ui.theme import DEFAULT_THEME, THEMES, ThemeName


pytestmark = pytest.mark.atomic


@pytest.fixture
def run_in_background(mocker: MockerFixture) -> Mock:
    return mocker.patch.object(_settings, "run_in_background")


@pytest.fixture
def screen(run_in_background) -> Iterator[_settings.SettingsScreen]:
    yield _settings.SettingsScreen()
    palette.apply_theme(DEFAULT_THEME)
    preferences.use_system_cursor = False


def _find_option(
    screen: _settings.SettingsScreen, theme_name: ThemeName
) -> _settings.ThemeOption:
    return next(
        option
        for option in screen.ids.themes.children
        if option.title == THEMES[theme_name].title
    )


def test_settings_lists_every_theme_by_its_title(screen):
    # when
    titles = [option.title for option in reversed(screen.ids.themes.children)]

    # then
    assert titles == [theme.title for theme in THEMES.values()]


def test_default_theme_is_marked_as_selected(screen):
    # when
    selected = [
        option.title for option in screen.ids.themes.children if option.selected
    ]

    # then
    assert selected == [THEMES[DEFAULT_THEME].title]


@pytest.mark.parametrize("theme_name", list(ThemeName))
def test_pressing_an_option_applies_and_selects_its_theme(screen, theme_name):
    # given
    option = _find_option(screen, theme_name)

    # when
    option.dispatch("on_release")

    # then
    assert (palette.theme_name, option.selected) == (theme_name, True)


def test_pressing_an_option_saves_the_theme_in_the_background(
    screen, run_in_background
):
    # given
    option = _find_option(screen, ThemeName.cherry_blossom)

    # when
    option.dispatch("on_release")
    task = run_in_background.call_args.args[0]

    # then
    assert (task.func, task.args) == (
        _settings.remember_theme,
        (ThemeName.cherry_blossom,),
    )


def test_ticking_system_cursor_applies_it_and_saves_it(
    screen, run_in_background
):
    # when
    screen.ids.system_cursor.active = True
    task = run_in_background.call_args.args[0]

    # then
    assert (preferences.use_system_cursor, task.func, task.keywords) == (
        True,
        _settings.remember_cursor_choice,
        {"use_system_cursor": True},
    )


def test_checkbox_shows_a_preference_changed_elsewhere(screen):
    # when
    preferences.use_system_cursor = True

    # then
    assert screen.ids.system_cursor.active is True


def test_preference_changed_elsewhere_is_not_saved_again(
    screen, run_in_background
):
    # when
    preferences.use_system_cursor = True

    # then
    assert run_in_background.called is False
