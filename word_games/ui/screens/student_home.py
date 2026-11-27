from pathlib import Path

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from word_games.ui import widgets  # noqa: F401  registers the kv widgets
from word_games.ui.student_route import StudentRoute


class StudentHomeScreen(Screen):
    def open_settings(self) -> None:
        self.manager.show(StudentRoute.settings)


Builder.load_file(str(Path(__file__).with_suffix(".kv")))
