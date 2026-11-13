"""Fill gaps: sentences with one or more gaps, each graded separately.

A sentence is stored as text segments with a gap between each neighbouring
pair, so "I ___ to school and ___ home." is
segments=["I ", " to school and ", " home."] with answers=["go", "come"].
Each gap is its own answer-key item: "{item_id}-{gap index}".
"""

from typing import Final, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    TypeAdapter,
    model_validator,
)

from word_games.game.model import (
    AnswerKey,
    GameEntry,
    ItemId,
    SplitContent,
    raise_if_duplicated_item_ids,
)


_item_id_adapter: Final[TypeAdapter[str]] = TypeAdapter(ItemId)


def gap_id(item_id: ItemId, gap_index: int) -> ItemId:
    return f"{item_id}-{gap_index}"


class GappedSentence(GameEntry):
    segments: list[str] = Field(min_length=2)
    answers: list[str] = Field(min_length=1)

    @model_validator(mode="after")
    def _one_answer_per_gap(self) -> Self:
        if len(self.segments) != len(self.answers) + 1:
            msg = "A sentence needs exactly one more segment than answers."
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def _gap_ids_are_valid(self) -> Self:
        _item_id_adapter.validate_python(
            gap_id(self.item_id, len(self.answers) - 1)
        )
        return self

    def answer_key(self) -> AnswerKey:
        return {
            gap_id(self.item_id, index): answer
            for index, answer in enumerate(self.answers)
        }


class FillGaps(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    sentences: list[GappedSentence] = Field(min_length=1)

    @model_validator(mode="after")
    def _item_ids_are_unique(self) -> Self:
        raise_if_duplicated_item_ids(s.item_id for s in self.sentences)
        return self

    def split_answers(self) -> SplitContent:
        public_sentences: list[JsonValue] = [
            sentence.model_dump(exclude={"answers"})
            for sentence in self.sentences
        ]
        return SplitContent(
            public={"sentences": public_sentences},
            answer_key={
                gap: answer
                for sentence in self.sentences
                for gap, answer in sentence.answer_key().items()
            },
        )
