from collections.abc import Iterator
from unittest.mock import MagicMock, call

import pytest
from pytest_mock import MockerFixture

from word_games.ui import preferences as _preferences
from word_games.ui.preferences import AppSettings
from word_games.ui.theme import ThemeName


pytestmark = pytest.mark.atomic


@pytest.fixture
def palette(mocker: MockerFixture) -> MagicMock:
    return mocker.patch.object(_preferences, "palette")


@pytest.fixture(autouse=True)
def reset_preferences() -> Iterator[None]:
    yield
    _preferences.preferences.use_system_cursor = False


@pytest.mark.parametrize("use_system_cursor", [True, False])
def test_apply_saved_settings(palette, use_system_cursor):
    # given
    settings = AppSettings(
        theme=ThemeName.cherry_blossom, use_system_cursor=use_system_cursor
    )

    # when
    _preferences.apply_saved_settings(settings)

    # then
    assert (
        palette.apply_theme.call_args_list,
        _preferences.preferences.use_system_cursor,
    ) == ([call(ThemeName.cherry_blossom)], use_system_cursor)
