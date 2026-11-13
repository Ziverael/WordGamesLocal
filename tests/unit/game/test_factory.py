import pytest

from word_games.error import InvalidGameContentError
from word_games.game import factory as _factory
from word_games.game.model import GameType
from word_games.game.quiz import Quiz


pytestmark = pytest.mark.atomic


def test_every_game_type_is_registered():
    # then
    assert set(_factory.GAME_BUILDERS) == set(GameType)


def test_create_game_builds_registered_class(quiz_content):
    # when
    game = _factory.create_game(GameType.quiz, quiz_content)

    # then
    assert isinstance(game, Quiz)


@pytest.mark.parametrize(
    "content",
    [
        pytest.param({}, id="empty"),
        pytest.param({"questions": "DROP TABLE"}, id="wrong-type"),
        pytest.param(None, id="none"),
    ],
)
def test_create_game_rejects_invalid_content(content):
    # when
    with pytest.raises(InvalidGameContentError) as error:
        _factory.create_game(GameType.quiz, content)

    # then
    assert error.match("quiz")


def test_crossword_stub_is_not_implemented():
    # given
    content = {
        "entries": [
            {
                "item_id": "e1",
                "clue": "Feline",
                "answer": "cat",
                "row": 0,
                "column": 0,
                "direction": "across",
            }
        ]
    }
    game = _factory.create_game(GameType.crossword, content)

    # when
    with pytest.raises(NotImplementedError) as error:
        game.split_answers()

    # then
    assert error.type is NotImplementedError
