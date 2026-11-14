# Word Games Local

Offline desktop application (Kivy) for word-game assignments.

- **Teachers** author an assignment, play it locally to test it, and export it to a file.
- **Students** import the file and play it in their client. No network is needed.

Exported files never contain plaintext answers: each answer is stored as a salted
`scrypt` digest, so the client can check a submission without revealing the key.

## Development

```sh
just init      # venv, .env, dev image
just run       # start the teacher client on the host
just run student   # start the student client on the host
just package   # build both clients into dist/ with PyInstaller
just test      # pytest in the wordgames-app-dev-helper container
just fc        # ruff format + ruff check + mypy
```

## Clients and releases

The project ships two separate applications built from one package:

| Client | Entry point | Purpose |
|---|---|---|
| `word-games-teacher` | `word_games/teacher/main.py` | author, test and export assignments |
| `word-games-student` | `word_games/student/main.py` | import and play assignments |

The student client must not import teacher-only code; `tests/unit/client/` guards this.

To publish a release, set `version` in `pyproject.toml`, merge to `main`, then push a
matching tag (`v1.2.3`). The CD workflow builds both clients for Linux, Windows and
macOS and attaches the zipped bundles to a GitHub Release. Pushes to `main` build the
same bundles as workflow artifacts only.
