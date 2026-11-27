"""Tile graphics.

There is one PNG set per theme. They are exported from the draw.io
sources in `design/icons/` with `just icons`. Edit the source, never
the PNG.
"""

from pathlib import Path
from typing import Final

from word_games.ui.theme import ThemeName


type IconName = str
type IconFile = str

_ICONS_DIR: Final = Path(__file__).parent / "assets" / "icons"

CROSSWORD: Final[IconName] = "crossword"
CROSSWORD_FREEFORM: Final[IconName] = "crossword_freeform"
CROSSWORD_CODEWORD: Final[IconName] = "crossword_codeword"
CROSSWORD_BLOCKED_GRID: Final[IconName] = "crossword_blocked_grid"
MATCHING: Final[IconName] = "matching"
QUIZ: Final[IconName] = "quiz"
FILL_GAPS: Final[IconName] = "fill_gaps"
MEMORY: Final[IconName] = "memory"
NEW_GAME: Final[IconName] = "new_game"


def locate_icon(name: IconName, theme_name: ThemeName) -> IconFile:
    return str(_ICONS_DIR / theme_name / f"{name}.png")
