from enum import StrEnum, auto
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt

from word_games.game.model import GameEntry, SplitContent


type Direction = Literal["across", "down"]


class CrosswordLayout(StrEnum):
    freeform = auto()
    codeword = auto()
    blocked_grid = auto()


class CrosswordEntry(GameEntry):
    clue: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    row: NonNegativeInt
    column: NonNegativeInt
    direction: Direction


class Crossword(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    entries: list[CrosswordEntry] = Field(min_length=1)

    def split_answers(self) -> SplitContent:
        msg = "Crossword is not implemented yet."
        raise NotImplementedError(msg)
