# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller build of both clients.

Run from the repository root:

    pyinstaller --noconfirm packaging/word_games.spec

Each client gets its own Analysis, so a bundle holds only what its entry
point imports and only the UI files (.kv, icons) listed for it. The student bundle
therefore carries no authoring screens.
"""

import sys
from pathlib import Path
from typing import NamedTuple

from kivy.tools.packaging.pyinstaller_hooks import (
    get_deps_minimal,
    hookspath,
    runtime_hooks,
)


PROJECT_ROOT = Path(SPECPATH).parent
UI_DIR = "word_games/ui"


class Client(NamedTuple):
    name: str
    entry_point: str
    ui_files: tuple[str, ...]


CLIENTS = (
    Client(
        name="word-games-teacher",
        entry_point="word_games/teacher/main.py",
        ui_files=(
            "widgets.kv",
            "screens/teacher_home.kv",
            "screens/game_picker.kv",
            "screens/editor.kv",
            "screens/settings.kv",
            "screens/player.kv",
            "assets/icons/*/*.png",
            "assets/cursors/*/*.png",
        ),
    ),
    Client(
        name="word-games-student",
        entry_point="word_games/student/main.py",
        ui_files=(
            "widgets.kv",
            "screens/student_home.kv",
            "screens/settings.kv",
            "screens/player.kv",
            "assets/cursors/*/*.png",
        ),
    ),
)


def windows_dependency_trees() -> list:
    """SDL2, GLEW and ANGLE DLLs are not Python imports, so Analysis misses them."""
    if sys.platform != "win32":
        return []
    from kivy_deps import angle, glew, sdl2

    return [
        Tree(path)
        for path in (*sdl2.dep_bins, *glew.dep_bins, *angle.dep_bins)
    ]


def collect_ui_files(client: Client) -> list[tuple[str, str]]:
    """Each entry of `ui_files` is a glob relative to the UI directory."""
    ui_dir = PROJECT_ROOT / UI_DIR
    return [
        (str(file), str(file.parent.relative_to(PROJECT_ROOT)))
        for pattern in client.ui_files
        for file in sorted(ui_dir.glob(pattern))
    ]


def build_client(client: Client) -> None:
    analysis = Analysis(
        [str(PROJECT_ROOT / client.entry_point)],
        pathex=[str(PROJECT_ROOT)],
        datas=collect_ui_files(client),
        hookspath=hookspath(),
        runtime_hooks=runtime_hooks(),
        **get_deps_minimal(video=None, audio=None),
    )
    executable = EXE(
        PYZ(analysis.pure),
        analysis.scripts,
        exclude_binaries=True,
        name=client.name,
        console=False,
    )
    bundle = COLLECT(
        executable,
        analysis.binaries,
        analysis.datas,
        *windows_dependency_trees(),
        name=client.name,
    )
    if sys.platform == "darwin":
        BUNDLE(
            bundle,
            name=f"{client.name}.app",
            bundle_identifier=f"local.wordgames.{client.name}",
        )


for client in CLIENTS:
    build_client(client)
