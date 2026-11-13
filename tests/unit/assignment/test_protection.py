import pytest
from pydantic import ValidationError

from word_games.assignment import protection as _protection
from word_games.assignment.model import ScryptParams


pytestmark = pytest.mark.atomic


@pytest.mark.parametrize(
    ("answer", "expected"),
    [
        pytest.param("Paris", "paris", id="case"),
        pytest.param("  New   York ", "new york", id="whitespace"),
        pytest.param("\uff21\uff22\uff23", "abc", id="fullwidth"),
        pytest.param("Straße", "strasse", id="casefold"),
        pytest.param("", "", id="empty"),
    ],
)
def test_normalize_answer(answer, expected):
    # when
    normalized = _protection.normalize_answer(answer)

    # then
    assert normalized == expected


def test_sealed_key_does_not_contain_answers(fast_scrypt_params):
    # when
    sealed = _protection.seal_answer_key({"q1": "Paris"}, fast_scrypt_params)

    # then
    assert "paris" not in sealed.model_dump_json().lower()


def test_equal_answers_in_different_items_have_different_digests(
    fast_scrypt_params,
):
    # when
    sealed = _protection.seal_answer_key(
        {"q1": "cat", "q2": "cat"}, fast_scrypt_params
    )

    # then
    assert sealed.digests["q1"] != sealed.digests["q2"]


@pytest.mark.parametrize(
    ("item_id", "answer", "expected"),
    [
        pytest.param("q1", "Paris", True, id="correct"),
        pytest.param("q1", " paris ", True, id="normalized"),
        pytest.param("q1", "Rome", False, id="wrong"),
        pytest.param("q9", "Paris", False, id="unknown-item"),
    ],
)
def test_is_answer_correct(fast_scrypt_params, item_id, answer, expected):
    # given
    sealed = _protection.seal_answer_key({"q1": "Paris"}, fast_scrypt_params)

    # when
    result = _protection.is_answer_correct(sealed, item_id, answer)

    # then
    assert result is expected


@pytest.mark.parametrize(
    "params",
    [
        pytest.param({"n": 2**30}, id="memory-exhaustion"),
        pytest.param({"n": 2**10 + 1}, id="not-power-of-two"),
        pytest.param({"r": 1000}, id="huge-block"),
    ],
)
def test_untrusted_scrypt_params_are_rejected(params):
    # when
    with pytest.raises(ValidationError) as error:
        ScryptParams.model_validate(params)

    # then
    assert error.type is ValidationError
