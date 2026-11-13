import pytest

from word_games.assignment import storage as _storage
from word_games.assignment.model import Assignment
from word_games.assignment.protection import seal_answer_key
from word_games.error import InvalidAssignmentFileError
from word_games.game.model import GameType


pytestmark = pytest.mark.atomic


@pytest.fixture
def assignment(fast_scrypt_params) -> Assignment:
    return Assignment(
        title="Geo",
        game_type=GameType.quiz,
        content={"questions": []},
        answer_key=seal_answer_key({"q1": "Paris"}, fast_scrypt_params),
    )


def test_saved_assignment_loads_back(tmp_path, assignment):
    # given
    path = tmp_path / "geo.json"
    _storage.save_assignment(assignment, path)

    # when
    loaded = _storage.load_assignment(path)

    # then
    assert loaded == assignment


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(b"not json", id="garbage"),
        pytest.param(b'{"title": "x"}', id="missing-fields"),
    ],
)
def test_invalid_file_is_rejected(tmp_path, payload):
    # given
    path = tmp_path / "bad.json"
    path.write_bytes(payload)

    # when
    with pytest.raises(InvalidAssignmentFileError) as error:
        _storage.load_assignment(path)

    # then
    assert error.type is InvalidAssignmentFileError


def test_oversized_file_is_rejected(tmp_path):
    # given
    path = tmp_path / "big.json"
    path.write_bytes(b" " * (_storage.MAX_ASSIGNMENT_FILE_BYTES + 1))

    # when
    with pytest.raises(InvalidAssignmentFileError) as error:
        _storage.load_assignment(path)

    # then
    assert error.match("exceeds")
