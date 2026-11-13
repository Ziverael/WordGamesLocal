import pytest
from pytest_mock import MockFixture

from word_games.assignment import controller as _controller
from word_games.assignment import protection as _protection
from word_games.game.model import GameType


pytestmark = pytest.mark.controller


@pytest.fixture
def fast_sealing(mocker: MockFixture, fast_scrypt_params):
    real_seal = _protection.seal_answer_key
    mocker.patch.object(
        _controller,
        "seal_answer_key",
        side_effect=lambda key: real_seal(key, fast_scrypt_params),
    )


@pytest.fixture
def assignment(fast_sealing, quiz_content):
    return _controller.create_assignment("Geo", GameType.quiz, quiz_content)


def test_create_assignment_keeps_answers_out_of_content(assignment):
    # then
    assert assignment.game_type == GameType.quiz
    assert "correct_option" not in str(assignment.content)
    assert set(assignment.answer_key.digests) == {"q1", "q2"}


@pytest.mark.parametrize(
    ("answers", "expected"),
    [
        pytest.param({"q1": "Paris", "q2": "4"}, (2, 2), id="all-correct"),
        pytest.param({"q1": "Paris", "q2": "5"}, (1, 2), id="one-wrong"),
        pytest.param({}, (0, 2), id="unanswered"),
        pytest.param({"q1": "Paris", "x": "4"}, (1, 2), id="unknown-item"),
    ],
)
def test_check_answers(assignment, answers, expected):
    # when
    score = _controller.check_answers(assignment, answers)

    # then
    assert score == expected
