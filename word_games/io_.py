"""Writing files so that a crash never leaves a half-written one behind."""

import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def write_text_atomically(text: str, path: Path) -> None:
    """Writes to a temporary file in the same folder, then swaps it in.

    The file is closed before the swap because Windows cannot rename an
    open file. UTF-8 is explicit because Windows defaults to cp1252.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(
        "w",
        encoding="utf-8",
        dir=path.parent,
        suffix=".tmp",
        delete_on_close=False,
    ) as tmp_file:
        tmp_file.write(text)
        tmp_file.flush()
        os.fsync(tmp_file.fileno())
        tmp_file.close()
        Path(tmp_file.name).replace(path)
