"""Teacher client: author an assignment, test it locally, export it."""

from kivy.app import App

from word_games.config.storage import load_settings
from word_games.ui.game_catalog import GAME_TILES
from word_games.ui.navigation import Navigator
from word_games.ui.preferences import apply_saved_settings
from word_games.ui.screens.editor import EditorScreen
from word_games.ui.screens.game_picker import GamePickerScreen
from word_games.ui.screens.settings import SettingsScreen
from word_games.ui.screens.teacher_home import TeacherHomeScreen
from word_games.ui.teacher_route import TeacherRoute
from word_games.ui.window import connect_window


def build_navigator() -> Navigator:
    game_types = GamePickerScreen(name=TeacherRoute.game_types)
    game_types.list_tiles("New Game", GAME_TILES)
    navigator = Navigator(TeacherRoute.home)
    for screen in (
        TeacherHomeScreen(name=TeacherRoute.home),
        game_types,
        GamePickerScreen(name=TeacherRoute.game_subtypes),
        EditorScreen(name=TeacherRoute.editor),
        SettingsScreen(name=TeacherRoute.settings),
    ):
        navigator.add_widget(screen)
    return navigator


class TeacherApp(App):
    title = "Word Games - Teacher"

    def build(self) -> Navigator:
        navigator = build_navigator()
        connect_window(navigator)
        return navigator


def run() -> None:
    apply_saved_settings(load_settings())
    TeacherApp().run()


if __name__ == "__main__":
    run()
