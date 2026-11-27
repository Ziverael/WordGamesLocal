from typing import Final

from kivy.app import App

from word_games.ui.navigation import Navigator


_ESCAPE: Final[int] = 27  # Also Back on Android


def esc_behaviour(navigator: Navigator, _window, key: int, *_args):
    if key != _ESCAPE:
        return False
    if navigator.is_main_menu():
        App.get_running_app().stop()
        return True
    navigator.go_back()
    return True
