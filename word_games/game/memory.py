from typing import Self

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from word_games.game.model import (
    GameEntry,
    SplitContent,
    raise_if_duplicated_item_ids,
)


class MatchingPair(GameEntry):
    first: str = Field(min_length=1)
    second: str = Field(min_length=1)


class Memory(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    pairs: list[MatchingPair] = Field(min_length=2)

    @model_validator(mode="after")
    def _item_ids_are_unique(self) -> Self:
        raise_if_duplicated_item_ids(pair.item_id for pair in self.pairs)
        return self

    def split_answers(self) -> SplitContent:
        cards: list[JsonValue] = [
            card for pair in self.pairs for card in (pair.first, pair.second)
        ]
        return SplitContent(
            public={"cards": cards},
            answer_key={pair.item_id: pair.second for pair in self.pairs},
        )
