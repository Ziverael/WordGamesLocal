from functools import partial

from word_games.assignment.controller import create_assignment
from word_games.ui.background import run_in_background


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
