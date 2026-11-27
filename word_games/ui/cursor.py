"""The mouse cursor, in the colours of the active theme.

Kivy cannot load a custom cursor image, so the system cursor is hidden
inside the window and a cursor image is drawn at the mouse position, on
the window's top canvas layer. Outside the window the system cursor
returns. The images are exported from `design/cursors/` with `just icons`.

With the "use system cursor" preference on, the operating system's own
cursor is used instead, which follows its size and contrast settings.
"""

from collections.abc import Mapping
from enum import StrEnum, auto
from pathlib import Path
from types import MappingProxyType
from typing import Final, NamedTuple, Protocol

from kivy.event import EventDispatcher
from kivy.graphics import (
    Canvas,
    Color,
    PopMatrix,
    PushMatrix,
    Rectangle,
    Translate,
)
from kivy.metrics import dp

from word_games.ui.theme import ThemeName


type Point = tuple[float, float]
type CursorFile = str


class CursorShape(StrEnum):
    arrow = auto()
    pointer = auto()
    text = auto()


class Hotspot(NamedTuple):
    """The point that clicks, in draw.io units from the top-left corner."""

    x: float
    y: float


# Every source is drawn on a 32 x 32 frame, shown 32 dp wide.
FRAME_UNITS: Final = 32
HOTSPOTS: Final[Mapping[CursorShape, Hotspot]] = MappingProxyType(
    {
        CursorShape.arrow: Hotspot(4, 3),
        CursorShape.pointer: Hotspot(13.5, 2),
        CursorShape.text: Hotspot(16, 16),
    }
)

SYSTEM_CURSORS: Final[Mapping[CursorShape, str]] = MappingProxyType(
    {
        CursorShape.arrow: "arrow",
        CursorShape.pointer: "hand",
        CursorShape.text: "ibeam",
    }
)

_CURSORS_DIR: Final = Path(__file__).parent / "assets" / "cursors"


def locate_cursor(shape: CursorShape, theme_name: ThemeName) -> CursorFile:
    return str(_CURSORS_DIR / theme_name / f"{shape}.png")


class CursorWindow(Protocol):
    canvas: Canvas
    show_cursor: bool

    def bind(self, **kwargs: object) -> object: ...

    def set_system_cursor(self, cursor_name: str) -> bool: ...


class ThemedCursor:
    def __init__(
        self,
        window: CursorWindow,
        palette: EventDispatcher,
        preferences: EventDispatcher,
    ) -> None:
        self._window = window
        self._palette = palette
        self._preferences = preferences
        self._position = Translate()
        # White leaves the image's own colours untinted.
        self._visibility = Color(1, 1, 1, 1)
        self._image = Rectangle()
        self._shape = CursorShape.arrow
        self._is_inside_window = True
        self._attach_to(window)
        self._redraw()

    def _attach_to(self, window: CursorWindow) -> None:
        for instruction in (
            PushMatrix(),
            self._position,
            self._visibility,
            self._image,
            PopMatrix(),
        ):
            window.canvas.after.add(instruction)
        window.bind(
            mouse_pos=self._follow_mouse,
            on_cursor_enter=self._enter_window,
            on_cursor_leave=self._leave_window,
        )
        self._palette.bind(theme_name=self._redraw)
        self._preferences.bind(use_system_cursor=self._redraw)

    def show(self, shape: CursorShape) -> None:
        if shape == self._shape:
            return
        self._shape = shape
        self._redraw()

    def _follow_mouse(self, _window: object, position: Point) -> None:
        self._position.xy = position

    def _enter_window(self, *_args: object) -> None:
        self._is_inside_window = True
        self._redraw()

    def _leave_window(self, *_args: object) -> None:
        self._is_inside_window = False
        self._redraw()

    def _redraw(self, *_args: object) -> None:
        use_system_cursor = self._preferences.use_system_cursor
        self._window.show_cursor = use_system_cursor
        self._visibility.a = (
            1 if self._is_inside_window and not use_system_cursor else 0
        )
        if use_system_cursor:
            self._window.set_system_cursor(SYSTEM_CURSORS[self._shape])
        else:
            self._place_image()

    def _place_image(self) -> None:
        """Places the image so that its hotspot sits on the mouse position."""
        side = dp(FRAME_UNITS)
        hotspot = HOTSPOTS[self._shape]
        self._image.source = locate_cursor(
            self._shape, self._palette.theme_name
        )
        self._image.size = (side, side)
        self._image.pos = (-dp(hotspot.x), dp(hotspot.y) - side)
