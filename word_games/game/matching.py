from random import sample
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from word_games.game.model import (
    GameEntry,
    SplitContent,
    raise_if_duplicated_item_ids,
)


class MatchingPair(GameEntry):
    left: str = Field(min_length=1)
    right: str = Field(min_length=1)


class Matching(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pairs: list[MatchingPair] = Field(min_length=2)

    @model_validator(mode="after")
    def _item_ids_are_unique(self) -> Self:
        raise_if_duplicated_item_ids(pair.item_id for pair in self.pairs)
        return self

    def split_answers(self) -> SplitContent:
        answers_key = {pair.item_id: pair.right for pair in self.pairs}
        lefts = [pair.left for pair in self.pairs]
        shuffled_rights = sample(
            [pair.right for pair in self.pairs], k=len(self.pairs)
        )
        rows: list[JsonValue] = [
            {"left": left, "right": right}
            for left, right in zip(lefts, shuffled_rights, strict=True)
        ]
        return SplitContent(
            public={"rows": rows},
            answer_key=answers_key,
        )
