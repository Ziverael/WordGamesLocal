import re
from typing import Final

import pytest

from design import export_icons
from word_games.ui import theme as _theme
from word_games.ui.theme import HexColour, ThemeColours, ThemeName


pytestmark = pytest.mark.atomic

_SOURCE_COLOUR: Final = re.compile(
    r"(?:fill|stroke|font)Color=(#[0-9A-Fa-f]{6})"
)
MINIMUM_TEXT_CONTRAST = 4.5
MINIMUM_GRAPHIC_CONTRAST = 3.0


def _measure_luminance(colour: HexColour) -> float:
    # the formula came from https://www.w3.org/WAI/WCAG21/Understanding/relative-luminance.html (accessed at: 2026-11-19)
    channels = [int(colour[index : index + 2], 16) / 255 for index in (1, 3, 5)]
    red, green, blue = (
        channel / 12.92
        if channel <= 0.03928
        else ((channel + 0.055) / 1.055) ** 2.4
        for channel in channels
    )
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


def _measure_contrast(first: HexColour, second: HexColour) -> float:
    darker, lighter = sorted(
        (_measure_luminance(first), _measure_luminance(second))
    )
    return (lighter + 0.05) / (darker + 0.05)


def test_every_theme_name_has_a_theme():
    # then
    assert set(_theme.THEMES) == set(ThemeName)


@pytest.mark.parametrize("theme_name", list(ThemeName))
@pytest.mark.parametrize(
    ("foreground", "background", "expected"),
    [
        pytest.param("text", "background", MINIMUM_TEXT_CONTRAST, id="text"),
        pytest.param(
            "text_muted", "background", MINIMUM_TEXT_CONTRAST, id="muted-text"
        ),
        pytest.param(
            "text",
            "surface_pressed",
            MINIMUM_TEXT_CONTRAST,
            id="text-on-selected",
        ),
        pytest.param(
            "accent", "surface", MINIMUM_GRAPHIC_CONTRAST, id="accent-graphics"
        ),
    ],
)
def test_theme_colours_are_readable(
    theme_name, foreground, background, expected
):
    # given
    colours = _theme.THEMES[theme_name].colours

    # when
    contrast = _measure_contrast(
        getattr(colours, foreground), getattr(colours, background)
    )

    # then
    assert contrast >= expected


def _collect_source_colours() -> set[HexColour]:
    """Exact text, not normalised: the export replaces colours as text, so a
    colour typed in lower case would slip through it unrecoloured.
    """
    return {
        colour
        for source in (export_icons.PROJECT_ROOT / "design").glob("*/*.drawio")
        for colour in _SOURCE_COLOUR.findall(source.read_text())
    }


def test_every_source_colour_has_a_theme_role():
    # when
    unmapped = _collect_source_colours() - set(export_icons.SOURCE_COLOUR_ROLES)

    # then
    assert unmapped == set()


def test_every_source_colour_role_is_a_theme_colour():
    # when
    unknown_roles = set(export_icons.SOURCE_COLOUR_ROLES.values()) - set(
        ThemeColours._fields
    )

    # then
    assert unknown_roles == set()
