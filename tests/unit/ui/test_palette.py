from collections.abc import Iterator

import pytest
from kivy.utils import get_color_from_hex

from word_games.ui import palette as _palette
from word_games.ui.theme import DEFAULT_THEME, THEMES, ThemeColours, ThemeName


pytestmark = pytest.mark.atomic


@pytest.fixture
def palette() -> Iterator[_palette.ActivePalette]:
    yield _palette.palette
    _palette.palette.apply_theme(DEFAULT_THEME)


def test_palette_starts_with_the_default_theme():
    # when
    fresh_palette = _palette.ActivePalette()

    # then
    assert fresh_palette.theme_name == DEFAULT_THEME


def test_palette_has_a_property_for_every_colour_role(palette):
    # when
    missing_roles = [
        role
        for role in ThemeColours._fields
        if palette.property(role, quiet=True) is None
    ]

    # then
    assert missing_roles == []


@pytest.mark.parametrize("theme_name", list(ThemeName))
def test_applied_theme_sets_every_colour_role(theme_name: ThemeName):
    # given
    palette = _palette.ActivePalette()
    expected = {
        role: get_color_from_hex(colour)
        for role, colour in THEMES[theme_name].colours._asdict().items()
    }

    # when
    palette.apply_theme(theme_name)

    # then
    assert {
        role: getattr(palette, role) for role in ThemeColours._fields
    } == expected
