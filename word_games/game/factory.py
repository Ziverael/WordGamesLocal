"""Game Factory.

Adding a game: implement the `Game` protocol in a Pydantic model and register
its `model_validate` below. A test guards that every `GameType` is registered.
"""

from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import Final

from pydantic import ValidationError

from word_games.error import InvalidGameContentError
from word_games.game.crossword import Crossword
from word_games.game.fill_gaps import FillGaps
from word_games.game.matching import Matching
from word_games.game.memory import Memory
from word_games.game.model import GameType
from word_games.game.protocol import Game
from word_games.game.quiz import Quiz


type GameBuilder = Callable[[object], Game]

GAME_BUILDERS: Final[Mapping[GameType, GameBuilder]] = MappingProxyType(
    {
        GameType.crossword: Crossword.model_validate,
        GameType.matching: Matching.model_validate,
        GameType.quiz: Quiz.model_validate,
        GameType.fill_gaps: FillGaps.model_validate,
        GameType.memory: Memory.model_validate,
    }
)


def create_game(game_type: GameType, authored_content: object) -> Game:
    build = GAME_BUILDERS[game_type]
    try:
        return build(authored_content)
    except ValidationError as error:
        msg = f"Invalid content for game {game_type}."
        raise InvalidGameContentError(msg) from error
