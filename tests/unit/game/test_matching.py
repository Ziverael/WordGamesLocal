import pytest

from word_games.game import matching as _matching


pytestmark = pytest.mark.atomic


@pytest.fixture
def matching() -> _matching.Matching:
    return _matching.Matching.model_validate(
        {
            "pairs": [
                {"item_id": "p1", "left": "dog", "right": "pies"},
                {"item_id": "p2", "left": "cat", "right": "kot"},
                {"item_id": "p3", "left": "fish", "right": "ryba"},
            ]
        }
    )


def test_split_answers_maps_left_ids_to_rights(matching):
    # when
    split = matching.split_answers()

    # then
    assert split.answer_key == {"p1": "pies", "p2": "kot", "p3": "ryba"}


def test_public_content_does_not_pair_lefts_with_rights(matching):
    # when
    split = matching.split_answers()

    # then
    assert "item_id" not in str(split.public["rows"][0])
    rights = [row["right"] for row in split.public["rows"]]
    assert sorted(rights) == ["kot", "pies", "ryba"]
