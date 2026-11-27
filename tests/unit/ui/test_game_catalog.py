from pathlib import Path

import pytest

from word_games.game.crossword import CrosswordLayout
from word_games.game.model import GameType
from word_games.ui import game_catalog as _game_catalog
from word_games.ui.game_catalog import GameSelection
from word_games.ui.icons import locate_icon
from word_games.ui.theme import ThemeName


pytestmark = pytest.mark.atomic


def test_every_game_type_has_exactly_one_tile():
    # when
    game_types = [tile.selection.game_type for tile in _game_catalog.GAME_TILES]

    # then
    assert sorted(game_types) == sorted(GameType)


def test_every_crossword_layout_is_a_subtype_tile():
    # given
    crossword = next(
        tile
        for tile in _game_catalog.GAME_TILES
        if tile.selection.game_type == GameType.crossword
    )

    # when
    layouts = [tile.selection.subtype for tile in crossword.subtypes]

    # then
    assert layouts == list(CrosswordLayout)


@pytest.mark.parametrize("theme_name", list(ThemeName))
def test_every_tile_has_an_icon_file_in_every_theme(theme_name):
    # when
    tiles_without_icon = [
        tile.title
        for game in _game_catalog.GAME_TILES
        for tile in (game, *game.subtypes)
        if not Path(locate_icon(tile.icon, theme_name)).is_file()
    ]

    # then
    assert tiles_without_icon == []


@pytest.mark.parametrize(
    ("selection", "expected"),
    [
        pytest.param(GameSelection(GameType.quiz), "Quiz", id="no-subtype"),
        pytest.param(
            GameSelection(GameType.crossword, CrosswordLayout.codeword),
            "Crossword: Codeword",
            id="subtype",
        ),
        pytest.param(
            GameSelection(GameType.crossword),
            "Crossword",
            id="subtype-not-chosen",
        ),
    ],
)
def test_describe_selection(selection, expected):
    # when
    description = _game_catalog.describe_selection(selection)

    # then
    assert description == expected
