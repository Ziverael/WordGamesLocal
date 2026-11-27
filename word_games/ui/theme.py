"""The colour themes a user can choose from.

The colours in use at runtime are held by `word_games.ui.palette`.
"""

from collections.abc import Mapping
from enum import StrEnum, auto
from types import MappingProxyType
from typing import Final, NamedTuple


type HexColour = str


class ThemeName(StrEnum):
    # Palletes based on those from https://coolors.co/palettes/trending (accessed at: 2026-11-15)
    summer_fun = auto()
    sunny_beach = auto()
    cherry_blossom = auto()
    vibrant_tones = auto()


class ThemeColours(NamedTuple):
    background: HexColour
    surface: HexColour
    surface_pressed: HexColour
    border: HexColour
    text: HexColour
    text_muted: HexColour
    accent: HexColour
    accent_dark: HexColour
    block: HexColour
    highlight: HexColour
    placeholder: HexColour


class Theme(NamedTuple):
    title: str
    colours: ThemeColours


THEMES: Final[Mapping[ThemeName, Theme]] = MappingProxyType(
    {
        ThemeName.summer_fun: Theme(
            "Refreshing Summer Fun",
            ThemeColours(
                background="#F3F9FC",
                surface="#FFFFFF",
                surface_pressed="#DDF0F8",
                border="#C3DEEA",
                text="#023047",
                text_muted="#4F6F80",
                accent="#219EBC",
                accent_dark="#023047",
                block="#023047",
                highlight="#FB8500",
                placeholder="#8ECAE6",
            ),
        ),
        ThemeName.sunny_beach: Theme(
            "Sunny Beach Day",
            ThemeColours(
                background="#FBF7EC",
                surface="#FFFFFF",
                surface_pressed="#DCEFEC",
                border="#E6DCC0",
                text="#264653",
                text_muted="#566F79",
                accent="#2A9D8F",
                accent_dark="#264653",
                block="#264653",
                highlight="#E76F51",
                placeholder="#E9C46A",
            ),
        ),
        ThemeName.cherry_blossom: Theme(
            "Cherry Blossom Bloom",
            ThemeColours(
                background="#FFF0F3",
                surface="#FFFFFF",
                surface_pressed="#FFCCD5",
                border="#FFB3C1",
                text="#590D22",
                text_muted="#A4133C",
                accent="#C9184A",
                accent_dark="#800F2F",
                block="#800F2F",
                highlight="#FF4D6D",
                placeholder="#FFB3C1",
            ),
        ),
        ThemeName.vibrant_tones: Theme(
            "Vibrant Tones",
            ThemeColours(
                background="#131A20",
                surface="#1F2933",
                surface_pressed="#2C3D4D",
                border="#3B4C5C",
                text="#F1F4F7",
                text_muted="#A9B9C8",
                accent="#63B6D9",
                accent_dark="#4D908E",
                block="#0A0F14",
                highlight="#F8961E",
                placeholder="#F9C74F",
            ),
        ),
    }
)

DEFAULT_THEME: Final = ThemeName.sunny_beach
