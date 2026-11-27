from typing import ClassVar, Final, Protocol
from weakref import WeakSet

from kivy.properties import BooleanProperty
from kivy.uix.widget import Widget

from word_games.ui.cursor import CursorShape


type WindowPosition = tuple[float, float]


class PointerWindow(Protocol):
    def bind(self, **kwargs: object) -> object: ...


class Cursor(Protocol):
    def show(self, shape: CursorShape) -> None: ...


# When several hovered widgets ask for different shapes, for example a
# text field inside a clickable row, the first one listed here wins.
_SHAPE_PRIORITY: Final = (CursorShape.text, CursorShape.pointer)


class HoverBehavior:
    """Mixin for a Widget: `hovered` is True while the pointer is over it."""

    hovered = BooleanProperty(defaultvalue=False)
    cursor_shape: ClassVar[CursorShape] = CursorShape.pointer
    instances: ClassVar[WeakSet["HoverBehavior"]] = WeakSet()

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        HoverBehavior.instances.add(self)


def is_pointer_over(widget: Widget, position: WindowPosition) -> bool:
    """A widget scrolled out of its container is drawn clipped, so every
    ancestor has to contain the pointer too.
    """
    window = widget.get_root_window()
    if window is None:
        return False
    node = widget
    while node is not None and node is not window:
        if not node.collide_point(*node.to_widget(*position)):
            return False
        node = node.parent
    return True


class PointerTracker:
    def __init__(self, window: PointerWindow, cursor: Cursor) -> None:
        self._cursor = cursor
        window.bind(mouse_pos=self._follow_pointer)

    def _follow_pointer(
        self, _window: PointerWindow, position: WindowPosition
    ) -> None:
        for widget in HoverBehavior.instances:
            widget.hovered = is_pointer_over(widget, position)
        self._show_cursor()

    def forget_hovered_widgets(self) -> None:
        """For screen changes: the pointer may not move, so no event follows."""
        for widget in HoverBehavior.instances:
            widget.hovered = False
        self._show_cursor()

    def _show_cursor(self) -> None:
        requested = {
            widget.cursor_shape
            for widget in HoverBehavior.instances
            if widget.hovered
        }
        self._cursor.show(
            next(
                (shape for shape in _SHAPE_PRIORITY if shape in requested),
                CursorShape.arrow,
            )
        )
