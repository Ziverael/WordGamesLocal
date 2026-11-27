"""What a teacher can create: one tile per game, with subtypes if any."""

from typing import Final, NamedTuple

from word_games.game.crossword import CrosswordLayout
from word_games.game.model import GameType
from word_games.ui import icons


type GameSubtype = CrosswordLayout


class GameSelection(NamedTuple):
    game_type: GameType
    subtype: GameSubtype | None = None


class GameTile(NamedTuple):
    title: str
    icon: icons.IconName
    selection: GameSelection
    subtypes: tuple["GameTile", ...] = ()


def _crossword_tile(
    title: str, icon: icons.IconName, layout: CrosswordLayout
) -> GameTile:
    return GameTile(title, icon, GameSelection(GameType.crossword, layout))


GAME_TILES: Final[tuple[GameTile, ...]] = (
    GameTile(
        "Crossword",
        icons.CROSSWORD,
        GameSelection(GameType.crossword),
        subtypes=(
            _crossword_tile(
                "Freeform", icons.CROSSWORD_FREEFORM, CrosswordLayout.freeform
            ),
            _crossword_tile(
                "Codeword", icons.CROSSWORD_CODEWORD, CrosswordLayout.codeword
            ),
            _crossword_tile(
                "Blocked Grid",
                icons.CROSSWORD_BLOCKED_GRID,
                CrosswordLayout.blocked_grid,
            ),
        ),
    ),
    GameTile("Matching", icons.MATCHING, GameSelection(GameType.matching)),
    GameTile("Quiz", icons.QUIZ, GameSelection(GameType.quiz)),
    GameTile(
        "Fill the Gaps", icons.FILL_GAPS, GameSelection(GameType.fill_gaps)
    ),
    GameTile("Memory", icons.MEMORY, GameSelection(GameType.memory)),
)


def describe_selection(selection: GameSelection) -> str:
    game = next(
        tile
        for tile in GAME_TILES
        if tile.selection.game_type == selection.game_type
    )
    subtype_titles = [
        tile.title for tile in game.subtypes if tile.selection == selection
    ]
    return ": ".join([game.title, *subtype_titles])
