from typing import Protocol

from word_games.game.model import SplitContent


class Game(Protocol):
    def split_answers(self) -> SplitContent: ...
