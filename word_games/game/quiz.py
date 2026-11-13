from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    NonNegativeInt,
    model_validator,
)

from word_games.game.model import (
    GameEntry,
    SplitContent,
    raise_if_duplicated_item_ids,
)


class QuizQuestion(GameEntry):
    prompt: str = Field(min_length=1)
    options: list[str] = Field(min_length=2)
    correct_option: NonNegativeInt

    @model_validator(mode="after")
    def _correct_option_exists(self) -> Self:
        if self.correct_option >= len(self.options):
            msg = "Correct option index is out of range."
            raise ValueError(msg)
        return self


class Quiz(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    questions: list[QuizQuestion] = Field(min_length=1)

    @model_validator(mode="after")
    def _item_ids_are_unique(self) -> Self:
        raise_if_duplicated_item_ids(q.item_id for q in self.questions)
        return self

    def split_answers(self) -> SplitContent:
        public_questions: list[JsonValue] = [
            question.model_dump(exclude={"correct_option"})
            for question in self.questions
        ]
        answer_key = {
            question.item_id: question.options[question.correct_option]
            for question in self.questions
        }
        return SplitContent(
            public={"questions": public_questions},
            answer_key=answer_key,
        )
