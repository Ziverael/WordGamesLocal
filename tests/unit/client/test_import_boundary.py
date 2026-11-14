import ast
from collections.abc import Iterator
from importlib.util import resolve_name
from pathlib import Path

import pytest

import word_games


pytestmark = pytest.mark.atomic

SOURCE_ROOT = Path(word_games.__file__).parent.parent
STUDENT_ENTRY_POINT = "word_games.student.main"
TEACHER_ONLY_MODULES: tuple[str, ...] = (
    "word_games.teacher",
    "word_games.ui.screens.editor",
)


def _find_source_file(module: str) -> Path | None:
    path = SOURCE_ROOT.joinpath(*module.split("."))
    candidates = (path.with_suffix(".py"), path / "__init__.py")
    return next((file for file in candidates if file.is_file()), None)


def _iter_imported_names(module: str, source: Path) -> Iterator[str]:
    package = (
        module if source.name == "__init__.py" else _get_parent_package(module)
    )
    for node in ast.walk(ast.parse(source.read_text())):
        if isinstance(node, ast.Import):
            yield from (alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            origin = resolve_name(
                "." * node.level + (node.module or ""), package
            )
            yield origin
            yield from (f"{origin}.{alias.name}" for alias in node.names)


def _get_parent_package(module: str) -> str:
    return module.rpartition(".")[0]


def _collect_reachable_names(entry_point: str) -> frozenset[str]:
    reachable: set[str] = set()
    pending = [entry_point]
    while pending:
        name = pending.pop()
        if not name or name in reachable:
            continue
        reachable.add(name)
        pending.append(_get_parent_package(name))
        source = _find_source_file(name)
        if source is not None:
            pending.extend(_iter_imported_names(name, source))
    return frozenset(reachable)


# Ast still do not resolve dynamic imports, like those with importlib.import_module()
@pytest.fixture(scope="module")
def names_reachable_from_student_client() -> frozenset[str]:
    return _collect_reachable_names(STUDENT_ENTRY_POINT)


def test_student_client_loads_its_entry_point(
    names_reachable_from_student_client,
):
    # then
    assert STUDENT_ENTRY_POINT in names_reachable_from_student_client


@pytest.mark.parametrize("teacher_only_module", TEACHER_ONLY_MODULES)
def test_student_client_does_not_load_teacher_code(
    names_reachable_from_student_client, teacher_only_module
):
    # when
    leaked = frozenset(
        name
        for name in names_reachable_from_student_client
        if f"{name}.".startswith(f"{teacher_only_module}.")
    )

    # then
    assert leaked == frozenset()
