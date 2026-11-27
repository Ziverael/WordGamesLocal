"""The colours in use right now.
`.kv` rules read them as `palette.text`, `palette.accent` and so on.
"""

from typing import Final

from kivy.event import EventDispatcher
from kivy.properties import ColorProperty, OptionProperty

from word_games.ui.theme import DEFAULT_THEME, THEMES, ThemeName


class ActivePalette(EventDispatcher):
    theme_name = OptionProperty(DEFAULT_THEME, options=THEMES.keys())
    background = ColorProperty()
    surface = ColorProperty()
    surface_pressed = ColorProperty()
    border = ColorProperty()
    text = ColorProperty()
    text_muted = ColorProperty()
    accent = ColorProperty()
    accent_dark = ColorProperty()
    block = ColorProperty()
    highlight = ColorProperty()
    placeholder = ColorProperty()

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.apply_theme(self.theme_name)

    def apply_theme(self, name: ThemeName) -> None:
        for role, colour in THEMES[name].colours._asdict().items():
            setattr(self, role, colour)
        self.theme_name = name


palette: Final = ActivePalette()
