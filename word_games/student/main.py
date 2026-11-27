"""Student client: import an assignment file and play it.

This module must never import teacher-only code. PyInstaller bundles
whatever is reachable from here, so an import of the editor would ship
the authoring screens to students.
"""

from kivy.app import App

from word_games.config.storage import load_settings
from word_games.ui.navigation import Navigator
from word_games.ui.preferences import apply_saved_settings
from word_games.ui.screens.settings import SettingsScreen
from word_games.ui.screens.student_home import StudentHomeScreen
from word_games.ui.student_route import StudentRoute
from word_games.ui.window import connect_window


def build_navigator() -> Navigator:
    navigator = Navigator(StudentRoute.home)
    navigator.add_widget(StudentHomeScreen(name=StudentRoute.home))
    navigator.add_widget(SettingsScreen(name=StudentRoute.settings))
    return navigator


class StudentApp(App):
    title = "Word Games - Student"

    def build(self) -> Navigator:
        navigator = build_navigator()
        connect_window(navigator)
        return navigator


def run() -> None:
    apply_saved_settings(load_settings())
    StudentApp().run()


if __name__ == "__main__":
    run()
