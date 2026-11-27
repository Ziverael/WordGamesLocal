"""User preferences in effect right now, other than colours.

Like `palette`, these are Kivy properties, so widgets that use them follow
changes made in Settings. Saved values are applied once at start-up.
"""

from typing import Final

from kivy.event import EventDispatcher
from kivy.properties import BooleanProperty

from word_games.config.app import AppSettings
from word_games.ui.palette import palette


class ActivePreferences(EventDispatcher):
    use_system_cursor = BooleanProperty(defaultvalue=False)


preferences: Final = ActivePreferences()


def apply_saved_settings(settings: AppSettings) -> None:
    palette.apply_theme(settings.theme)
    preferences.use_system_cursor = settings.use_system_cursor
