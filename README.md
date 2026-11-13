# Word Games Local

Offline desktop application (Kivy) for word-game assignments.

- **Teachers** author an assignment, play it locally to test it, and export it to a file.
- **Students** import the file and play it in their client. No network is needed.

Exported files never contain plaintext answers: each answer is stored as a salted
`scrypt` digest, so the client can check a submission without revealing the key.

## Development

```sh
just init      # venv, .env, dev image
just run       # start the desktop app on the host
just test      # pytest in the wordgames-app-dev-helper container
just fc        # ruff format + ruff check + mypy
```
