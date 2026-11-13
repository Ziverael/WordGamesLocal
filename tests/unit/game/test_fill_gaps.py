import pytest
from pydantic import ValidationError

from word_games.game import fill_gaps as _fill_gaps


pytestmark = pytest.mark.atomic


@pytest.fixture
def fill_gaps() -> _fill_gaps.FillGaps:
    return _fill_gaps.FillGaps.model_validate(
        {
            "sentences": [
                {
                    "item_id": "s1",
                    "segments": ["I ", " to school and ", " home."],
                    "answers": ["go", "come"],
                },
                {
                    "item_id": "s2",
                    "segments": ["The ", " sat."],
                    "answers": ["cat"],
                },
            ]
        }
    )


def test_split_answers_keys_every_gap(fill_gaps):
    # when
    split = fill_gaps.split_answers()

    # then
    assert split.answer_key == {"s1-0": "go", "s1-1": "come", "s2-0": "cat"}


def test_public_content_has_no_answers(fill_gaps):
    # when
    split = fill_gaps.split_answers()

    # then
    assert "answers" not in str(split.public)
    assert "come" not in str(split.public)


@pytest.mark.parametrize(
    ("sentence", "expected"),
    [
        pytest.param(
            {"item_id": "s1", "segments": ["a ", " b"], "answers": ["x", "y"]},
            "one more segment",
            id="too-many-answers",
        ),
        pytest.param(
            {"item_id": "s1", "segments": ["a", "b", "c"], "answers": ["x"]},
            "one more segment",
            id="too-few-answers",
        ),
        pytest.param(
            {"item_id": "s" * 64, "segments": ["a", "b"], "answers": ["x"]},
            "at most 64",
            id="gap-id-too-long",
        ),
    ],
)
def test_invalid_sentence_is_rejected(sentence, expected):
    # when
    with pytest.raises(ValidationError) as error:
        _fill_gaps.GappedSentence.model_validate(sentence)

    # then
    assert error.match(expected)


def test_duplicated_sentence_ids_are_rejected():
    # given
    sentence = {"item_id": "s1", "segments": ["a", "b"], "answers": ["x"]}

    # when
    with pytest.raises(ValidationError) as error:
        _fill_gaps.FillGaps.model_validate({"sentences": [sentence, sentence]})

    # then
    assert error.match("unique")
