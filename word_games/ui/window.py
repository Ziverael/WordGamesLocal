"""Hooks between the application window and the UI, shared by both clients.

Importing this module creates the window, so only the client entry
points may import it.
"""

from functools import partial

from kivy.core.window import Window

from word_games.ui.cursor import ThemedCursor
from word_games.ui.hover import PointerTracker
from word_games.ui.keyboard import esc_behaviour
from word_games.ui.navigation import Navigator
from word_games.ui.palette import palette
from word_games.ui.preferences import preferences


def connect_window(navigator: Navigator) -> None:
    Window.clearcolor = palette.background
    palette.bind(background=Window.setter("clearcolor"))
    pointer = PointerTracker(Window, ThemedCursor(Window, palette, preferences))
    navigator.bind(current=lambda *_args: pointer.forget_hovered_widgets())
    Window.bind(on_keyboard=partial(esc_behaviour, navigator))
