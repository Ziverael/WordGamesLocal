# Word Games Local

Offline desktop application for language teachers: they author assignments, play them locally to test them, and export them to a file. Students import the file and play it in their own client.

General engineering, Python and testing conventions live in `.claude/rules/`. This file holds only the facts of this project.

## Stack

Python, `Kivy`. Must run on Linux, Windows 10/11 and macOS. The program should have an installer.

## Commands

Run in container `wordgames-app-dev-helper`. The `just` recipes are started from the host and enter the container themselves.
- tests: `just test <path>`; filter by marker with `just test ./tests "-m atomic"` (single-word filters only)
- lint + check: `just fc`
- desktop clients: `just run` (teacher) or `just run student` (on the host, needs a display)
- client bundles: `just package` (PyInstaller, output in `dist/`)

## Layout

- source package: `word_games/`
- tests: `tests/unit/`, `tests/component/`

## Architecture

- **Clients:** two applications from one package, `teacher/main.py` and `student/main.py`. The student client never imports teacher-only code, because PyInstaller bundles whatever its entry point imports.
- **Layers:** Kivy UI (`<client>/main.py`, `ui/`) → `<domain>/controller.py` → `<domain>/storage.py`, `<domain>/protection.py`, `<domain>/model.py`. Domains never import Kivy. No business logic in UI code.
- **Trust boundaries:** imported assignment files are untrusted. Check size limits, Pydantic validation and bounded KDF parameters. No plaintext answer may reach an exported file.
- **Persistence:** assignment files only, no database. A change to `Assignment` bumps `schema_version`; older files stay loadable or are rejected with a clear error.
- **Slow operations:** scrypt and file I/O must not run on the Kivy UI thread.

## Testing notes

- Use the `fast_scrypt_params` fixture from `tests/conftest.py` wherever answers are sealed; the default cost is deliberately slow.
- Test file persistence with `tmp_path`.
- `polyfactory` is available for factories in `tests/conftest.py`.
- e2e tests are not set up; adding pytest-bdd or a GUI driver needs approval first.
