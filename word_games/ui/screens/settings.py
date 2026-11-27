import logging
from collections.abc import Sequence
from functools import partial
from pathlib import Path
from typing import Final

from kivy.lang import Builder
from kivy.properties import BooleanProperty, ColorProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from word_games.config.controller import (
    remember_cursor_choice,
    remember_theme,
)
from word_games.ui import widgets  # noqa: F401  registers the kv widgets
from word_games.ui.background import run_in_background
from word_games.ui.hover import HoverBehavior
from word_games.ui.palette import palette
from word_games.ui.preferences import preferences
from word_games.ui.theme import THEMES, HexColour, ThemeColours, ThemeName


_logger: Final = logging.getLogger(__name__)


def _report_unsaved_setting(error: Exception) -> None:
    """The change still applies for this session; only remembering it failed."""
    _logger.warning("Could not save the setting: %s", error)


def pick_swatches(colours: ThemeColours) -> Sequence[HexColour]:
    """Colours that preview a theme in its settings row."""
    return (
        colours.accent,
        colours.text,
        colours.highlight,
        colours.placeholder,
    )


class Swatch(Widget):
    color = ColorProperty()


class ThemeOption(HoverBehavior, ButtonBehavior, BoxLayout):
    title = StringProperty()
    selected = BooleanProperty(defaultvalue=False)

    def show_swatches(self, colours: Sequence[HexColour]) -> None:
        for colour in colours:
            self.ids.swatches.add_widget(Swatch(color=colour))


class CheckOption(HoverBehavior, ButtonBehavior, BoxLayout):
    """A row with a checkbox; clicking anywhere on it toggles `active`."""

    title = StringProperty()
    description = StringProperty()
    active = BooleanProperty(defaultvalue=False)


class SettingsScreen(Screen):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.setup_theme_options()

    def setup_theme_options(self) -> None:
        self._theme_options = {
            name: self._build_theme_option(name) for name in THEMES
        }
        for option in self._theme_options.values():
            self.ids.themes.add_widget(option)
        palette.bind(theme_name=self._mark_selected_option)
        self._mark_selected_option(palette, palette.theme_name)

    def _build_theme_option(self, name: ThemeName) -> ThemeOption:
        theme = THEMES[name]
        option = ThemeOption(title=theme.title)
        option.show_swatches(pick_swatches(theme.colours))
        option.bind(on_release=partial(self._apply_theme, name))
        return option

    def _apply_theme(self, name: ThemeName, _option: ThemeOption) -> None:
        palette.apply_theme(name)
        run_in_background(
            partial(remember_theme, name),
            on_done=lambda _settings: None,
            on_error=_report_unsaved_setting,
        )

    def _mark_selected_option(
        self, _palette: object, theme_name: ThemeName
    ) -> None:
        for name, option in self._theme_options.items():
            option.selected = name == theme_name

    def apply_cursor_choice(self, *, active: bool) -> None:
        if active == preferences.use_system_cursor:
            return
        preferences.use_system_cursor = active
        run_in_background(
            partial(remember_cursor_choice, use_system_cursor=active),
            on_done=lambda _settings: None,
            on_error=_report_unsaved_setting,
        )


Builder.load_file(str(Path(__file__).with_suffix(".kv")))
