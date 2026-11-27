"""Tile menu of games. One instance lists game types, another subtypes."""

from collections.abc import Sequence
from functools import partial
from pathlib import Path

from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen

from word_games.ui.game_catalog import GameTile
from word_games.ui.teacher_route import TeacherRoute
from word_games.ui.widgets import Tile


class GamePickerScreen(Screen):
    heading = StringProperty()

    def list_tiles(self, heading: str, tiles: Sequence[GameTile]) -> None:
        self.heading = heading
        self.ids.grid.clear_widgets()
        for tile in tiles:
            self.ids.grid.add_widget(self._build_tile(tile))

    def _build_tile(self, tile: GameTile) -> Tile:
        widget = Tile(title=tile.title, icon=tile.icon)
        widget.bind(on_release=partial(self._select_tile, tile))
        return widget

    def _select_tile(self, tile: GameTile, _widget: Tile) -> None:
        if tile.subtypes:
            self._open_subtypes(tile)
        else:
            self._open_editor(tile)

    def _open_subtypes(self, tile: GameTile) -> None:
        subtypes = self.manager.get_screen(TeacherRoute.game_subtypes)
        subtypes.list_tiles(tile.title, tile.subtypes)
        self.manager.show(TeacherRoute.game_subtypes)

    def _open_editor(self, tile: GameTile) -> None:
        editor = self.manager.get_screen(TeacherRoute.editor)
        editor.edit_new_game(tile.selection)
        self.manager.show(TeacherRoute.editor)


Builder.load_file(str(Path(__file__).with_suffix(".kv")))
