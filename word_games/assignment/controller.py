"""Assignment use cases.

Teachers test an assignment through the same sealed path students use,
so "run locally" exercises exactly what will be exported.
"""

from word_games.assignment.model import Assignment, Score, StudentAnswers
from word_games.assignment.protection import is_answer_correct, seal_answer_key
from word_games.game.factory import create_game
from word_games.game.model import GameType


def create_assignment(
    title: str, game_type: GameType, authored_content: object
) -> Assignment:
    game = create_game(game_type, authored_content)
    public, answer_key = game.split_answers()
    return Assignment(
        title=title,
        game_type=game_type,
        content=public,
        answer_key=seal_answer_key(answer_key),
    )


def check_answers(assignment: Assignment, answers: StudentAnswers) -> Score:
    correct = sum(
        is_answer_correct(
            assignment.answer_key, item_id, answers.get(item_id, "")
        )
        for item_id in assignment.answer_key.digests
    )
    return Score(correct=correct, total=len(assignment.answer_key.digests))
