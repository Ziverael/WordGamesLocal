"""Vocabulary shared by every game.

A game's authored content (written by a teacher) contains the answers.
Before export it is split into public content, which the student sees,
and an answer key, which is sealed (see `word_games.assignment.protection`).
"""

from collections import Counter
from collections.abc import Iterable
from enum import StrEnum, auto
from typing import Annotated, NamedTuple

from pydantic import BaseModel, ConfigDict, Field, JsonValue


class GameType(StrEnum):
    crossword = auto()
    matching = auto()
    quiz = auto()
    fill_gaps = auto()
    memory = auto()


type ItemId = Annotated[
    str, Field(min_length=1, max_length=64, pattern=r"^[A-Za-z0-9_-]+$")
]
type Answer = str
type AnswerKey = dict[ItemId, Answer]
type PublicContent = dict[str, JsonValue]


class GameEntry(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")
    item_id: ItemId


class SplitContent(NamedTuple):
    public: PublicContent
    answer_key: AnswerKey


def raise_if_duplicated_item_ids(item_ids: Iterable[ItemId]) -> None:
    duplicates = [
        item_id for item_id, count in Counter(item_ids).items() if count > 1
    ]
    if duplicates:
        msg = f"Item ids must be unique, duplicated: {duplicates}."
        raise ValueError(msg)
