from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Final

from pydantic import ValidationError

from word_games.assignment.model import Assignment
from word_games.error import InvalidAssignmentFileError


_MAX_ASSIGNMENT_FILE_BYTES: Final = 5 * 1024 * 1024


def save_assignment(assignment: Assignment, path: Path) -> None:
    with NamedTemporaryFile("w", dir=path.parent) as tmp_file:
        tmp_file.write(assignment.model_dump_json(indent=2))
        tmp_file.flush()
        Path(tmp_file.name).replace(path)


def load_assignment(path: Path) -> Assignment:
    raise_if_file_too_large(path)
    try:
        return Assignment.model_validate_json(path.read_bytes())
    except ValidationError as error:
        msg = f"{path.name} is not a valid assignment file."
        raise InvalidAssignmentFileError(msg) from error


def raise_if_file_too_large(path: Path) -> None:
    if path.stat().st_size > _MAX_ASSIGNMENT_FILE_BYTES:
        msg = f"{path.name} exceeds {_MAX_ASSIGNMENT_FILE_BYTES} bytes."
        raise InvalidAssignmentFileError(msg)
