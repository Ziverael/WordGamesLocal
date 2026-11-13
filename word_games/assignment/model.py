"""The assignment file exchanged between teacher and student.

Students import files they did not create, so every field is validated,
including the scrypt cost: unbounded parameters would let a crafted file
exhaust the student's memory.
"""

from typing import Annotated, Final, Literal, NamedTuple, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
    model_validator,
)

from word_games.game.model import GameType, ItemId, PublicContent


_MIN_SCRYPT_COST: Final = 2**10
_MAX_SCRYPT_COST: Final = 2**15

type HexBytes = Annotated[str, Field(pattern=r"^([0-9a-f]{2})+$")]
type ScryptCost = Annotated[
    int, Field(ge=_MIN_SCRYPT_COST, le=_MAX_SCRYPT_COST)
]
type StudentAnswers = dict[ItemId, str]


class ScryptParams(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    n: ScryptCost = 2**14
    r: Annotated[int, Field(ge=1, le=8)] = 8
    p: Annotated[int, Field(ge=1, le=2)] = 1

    @model_validator(mode="after")
    def _cost_is_power_of_two(self) -> Self:
        if self.n & (self.n - 1):
            msg = "Scrypt cost must be a power of two."
            raise ValueError(msg)
        return self


class SealedAnswerKey(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    salt: HexBytes
    params: ScryptParams
    digests: dict[ItemId, HexBytes] = Field(min_length=1)


class Assignment(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: Literal[1] = 1
    title: str = Field(min_length=1, max_length=200)
    game_type: GameType
    content: PublicContent
    answer_key: SealedAnswerKey


class Score(NamedTuple):
    correct: NonNegativeInt
    total: NonNegativeInt
