import pytest

from word_games.assignment.model import _MIN_SCRYPT_COST, ScryptParams


@pytest.fixture
def fast_scrypt_params() -> ScryptParams:
    return ScryptParams(n=_MIN_SCRYPT_COST, r=1, p=1)


@pytest.fixture
def quiz_content() -> dict[str, object]:
    return {
        "questions": [
            {
                "item_id": "q1",
                "prompt": "Capital of France?",
                "options": ["Paris", "Rome"],
                "correct_option": 0,
            },
            {
                "item_id": "q2",
                "prompt": "2 + 2?",
                "options": ["3", "4", "5"],
                "correct_option": 1,
            },
        ]
    }
