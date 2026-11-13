import pytest
from pydantic import ValidationError

from word_games.game import quiz as _quiz


pytestmark = pytest.mark.atomic


def test_split_answers_removes_correct_option_from_public(quiz_content):
    # given
    quiz = _quiz.Quiz.model_validate(quiz_content)

    # when
    split = quiz.split_answers()

    # then
    assert "correct_option" not in str(split.public)
    assert split.answer_key == {"q1": "Paris", "q2": "4"}


@pytest.mark.parametrize(
    ("change", "expected"),
    [
        pytest.param({"correct_option": 5}, "out of range", id="out-of-range"),
        pytest.param({"options": ["only"]}, "at least 2", id="one-option"),
        pytest.param({"item_id": "q 1"}, "pattern", id="unsafe-id"),
    ],
)
def test_invalid_question_is_rejected(quiz_content, change, expected):
    # given
    question = quiz_content["questions"][0] | change

    # when
    with pytest.raises(ValidationError) as error:
        _quiz.QuizQuestion.model_validate(question)

    # then
    assert error.match(expected)


def test_duplicated_item_ids_are_rejected(quiz_content):
    # given
    question = quiz_content["questions"][0]

    # when
    with pytest.raises(ValidationError) as error:
        _quiz.Quiz.model_validate({"questions": [question, question]})

    # then
    assert error.match("unique")
