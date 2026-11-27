from pathlib import Path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from word_games.ui import widgets  # noqa: F401  registers the kv widgets
from word_games.ui.teacher_route import TeacherRoute


class TeacherHomeScreen(Screen):
    def start_new_game(self) -> None:
        self.manager.show(TeacherRoute.game_types)

    def open_settings(self) -> None:
        self.manager.show(TeacherRoute.settings)


Builder.load_file(str(Path(__file__).with_suffix(".kv")))
