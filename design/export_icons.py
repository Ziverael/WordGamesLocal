"""Export the draw.io graphics in `design/` to one PNG set per theme.

Run with `just icons`; it needs draw.io on the host. Themes whose
sources and colours are unchanged since the last export are skipped; pass
`--force` to export everything. The sources are
drawn in eight fixed colours, each standing for one theme colour role, and
are recoloured for every theme before export. Tile icons come from
`design/icons/` and mouse cursors from `design/cursors/`.
"""

import hashlib
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Final, NamedTuple

from word_games.ui.theme import THEMES, HexColour, ThemeColours


PROJECT_ROOT: Final = Path(__file__).parent.parent
ASSETS_DIR: Final = PROJECT_ROOT / "word_games" / "ui" / "assets"
# The draw.io snap cannot read the system temp directory.
WORK_DIR: Final = PROJECT_ROOT / ".local" / "icon-export"
# Fingerprints of the last export per theme; not committed, so a fresh
# clone exports everything once.
STAMPS_DIR: Final = PROJECT_ROOT / ".local" / "icon-export-stamps"


class AssetSet(NamedTuple):
    """`design/<name>/*.drawio` is exported to `assets/<name>/<theme>/`."""

    name: str
    pixels: int


ASSET_SETS: Final = (
    AssetSet("icons", pixels=256),
    # Cursors are drawn on a 32-unit frame and shown 32 dp wide, so 64 px
    # stays sharp on high-density screens.
    AssetSet("cursors", pixels=64),
)

SOURCE_COLOUR_ROLES: Final[Mapping[HexColour, str]] = MappingProxyType(
    {
        "#2966D1": "accent",
        "#1B4594": "accent_dark",
        # Blocked crossword cells: dark in every theme, like a printed puzzle.
        "#0B1F4B": "block",
        "#DEE8FA": "surface_pressed",
        "#212633": "text",
        "#F2A33A": "highlight",
        "#B9C3D6": "placeholder",
        # Cell and card fills, and letters on the accent colour.
        "#FFFFFF": "surface",
    }
)


def recolour(drawing: str, colours: ThemeColours) -> str:
    """Two passes: a theme colour may equal another source colour, and
    replacing in one pass would then recolour it a second time.
    """
    for source_colour, role in SOURCE_COLOUR_ROLES.items():
        drawing = drawing.replace(source_colour, f"@{role}@")
    for role in SOURCE_COLOUR_ROLES.values():
        drawing = drawing.replace(f"@{role}@", getattr(colours, role))
    return drawing


def write_recoloured_sources(
    sources: Path, colours: ThemeColours, target: Path
) -> None:
    target.mkdir(parents=True)
    for source in sources.glob("*.drawio"):
        recoloured = recolour(source.read_text(), colours)
        (target / source.name).write_text(recoloured)


def export_to_png(sources: Path, target: Path, pixels: int) -> None:
    target.mkdir(parents=True, exist_ok=True)
    subprocess.run(  # noqa: S603
        [  # noqa: S607
            "drawio",
            "--export",
            "--format",
            "png",
            "--transparent",
            "--width",
            str(pixels),
            "--border",
            "0",
            "--output",
            str(target),
            str(sources),
        ],
        check=True,
    )


def fingerprint_export(
    sources: Path, colours: ThemeColours, pixels: int
) -> str:
    """Everything that changes the exported images, this script included."""
    digest = hashlib.sha256()
    digest.update(Path(__file__).read_bytes())
    digest.update(repr((pixels, tuple(colours))).encode())
    for source in sorted(sources.glob("*.drawio")):
        digest.update(source.name.encode())
        digest.update(source.read_bytes())
    return digest.hexdigest()


def is_export_current(
    stamp: Path, fingerprint: str, sources: Path, target: Path
) -> bool:
    """The images must also exist: one may have been deleted by hand."""
    return (
        stamp.is_file()
        and stamp.read_text() == fingerprint
        and all(
            (target / f"{source.stem}.png").is_file()
            for source in sources.glob("*.drawio")
        )
    )


def export_theme(
    asset_set: AssetSet, theme_name: str, colours: ThemeColours
) -> None:
    work_dir = WORK_DIR / asset_set.name / theme_name
    write_recoloured_sources(
        PROJECT_ROOT / "design" / asset_set.name, colours, work_dir
    )
    export_to_png(
        work_dir, ASSETS_DIR / asset_set.name / theme_name, asset_set.pixels
    )


def export_all_themes(*, force: bool = False) -> None:
    """Exports only themes whose fingerprint changed, unless forced."""
    shutil.rmtree(WORK_DIR, ignore_errors=True)
    for asset_set in ASSET_SETS:
        sources = PROJECT_ROOT / "design" / asset_set.name
        for name, theme in THEMES.items():
            stamp = STAMPS_DIR / asset_set.name / f"{name}.sha256"
            fingerprint = fingerprint_export(
                sources, theme.colours, asset_set.pixels
            )
            target = ASSETS_DIR / asset_set.name / name
            if not force and is_export_current(
                stamp, fingerprint, sources, target
            ):
                print(f"{asset_set.name}/{name}: up to date")  # noqa: T201
                continue
            export_theme(asset_set, name, theme.colours)
            stamp.parent.mkdir(parents=True, exist_ok=True)
            stamp.write_text(fingerprint)
            print(f"{asset_set.name}/{name}: exported")  # noqa: T201
    shutil.rmtree(WORK_DIR, ignore_errors=True)


if __name__ == "__main__":
    export_all_themes(force="--force" in sys.argv[1:])
