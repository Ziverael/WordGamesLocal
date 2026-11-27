from functools import partial
from pathlib import Path

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen

from word_games.assignment.controller import create_assignment
from word_games.ui import widgets  # noqa: F401  registers the kv widgets
from word_games.ui.background import run_in_background
from word_games.ui.game_catalog import GameSelection, describe_selection


class EditorScreen(Screen):
    heading = StringProperty()
    selection = ObjectProperty(None, allownone=True)

    def edit_new_game(self, selection: GameSelection) -> None:
        self.selection = selection
        self.heading = f"New {describe_selection(selection)}"
        self.ids.title.text = ""


def on_export_pressed(self) -> None:
    self.busy = True
    run_in_background(
        partial(
            create_assignment,
            self.title,
            self.game_type,
            self.collect_content(),
        ),
        on_done=self._save_and_confirm,
        on_error=self._show_error,
    )


Builder.load_file(str(Path(__file__).with_suffix(".kv")))
