"""Widgets shared by the screens. Their layout is in `widgets.kv`.

`icons` and `palette` are imported here although only `widgets.kv` uses
them: PyInstaller bundles what Python imports and cannot see a `.kv`
import.
"""

from functools import partial
from math import cos, pi, sin
from pathlib import Path
from typing import Final

from kivy.animation import Animation
from kivy.graphics import Color, Line
from kivy.lang import Builder
from kivy.properties import ColorProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from word_games.ui import icons, palette  # noqa: F401
from word_games.ui.cursor import CursorShape
from word_games.ui.hover import HoverBehavior


_POP_UP_SCALE: Final = 1.2
_POP_UP_TILT_DEGREES: Final = 20
_SETTLE_SECONDS: Final = 0.15
_GEAR_TEETH: Final = 8


def build_pop_up_animation() -> Animation:
    """Played once: grow, rock left-right-left, then stay grown.

    The tile shrinks back only when the hover ends (see `Tile.on_hovered`).
    """
    step = partial(Animation, transition="in_out_quad")
    return (
        step(scale=_POP_UP_SCALE, duration=0.1)
        + step(rotation=_POP_UP_TILT_DEGREES, duration=0.06)
        + step(rotation=-_POP_UP_TILT_DEGREES, duration=0.06)
        + step(rotation=_POP_UP_TILT_DEGREES, duration=0.06)
        + step(rotation=0, duration=0.1)
    )


class Tile(HoverBehavior, ButtonBehavior, BoxLayout):
    title = StringProperty()
    icon = StringProperty()
    scale = NumericProperty(1)
    rotation = NumericProperty(0)

    def on_hovered(self, _tile: "Tile", hovered: bool) -> None:  # noqa: FBT001
        Animation.cancel_all(self, "scale", "rotation")
        if hovered:
            self._draw_above_siblings()
            build_pop_up_animation().start(self)
        else:
            Animation(scale=1, rotation=0, duration=_SETTLE_SECONDS).start(self)

    def _draw_above_siblings(self) -> None:
        """A waving tile overlaps its neighbours. Moving its canvas to the
        end of the parent's canvas changes the drawing order only; moving
        the widget itself would change its place in the grid.
        """
        if self.parent is None:
            return
        self.parent.canvas.remove(self.canvas)
        self.parent.canvas.add(self.canvas)


class BackButton(HoverBehavior, ButtonBehavior, Widget):
    pass


class GearButton(HoverBehavior, ButtonBehavior, Widget):
    """A gear drawn as a ring with square teeth, in the given colour."""

    color = ColorProperty()

    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw, color=self._redraw)

    def _redraw(self, *_args: object) -> None:
        radius = min(self.width, self.height) * 0.3
        self.canvas.clear()
        with self.canvas:
            Color(rgba=self.color)
            Line(
                circle=(self.center_x, self.center_y, radius * 0.62),
                width=radius * 0.24,
            )
            for tooth in range(_GEAR_TEETH):
                self._draw_tooth(2 * pi * tooth / _GEAR_TEETH, radius)

    def _draw_tooth(self, angle: float, radius: float) -> None:
        reach_x, reach_y = cos(angle) * radius, sin(angle) * radius
        Line(
            points=[
                self.center_x + reach_x * 0.86,
                self.center_y + reach_y * 0.86,
                self.center_x + reach_x,
                self.center_y + reach_y,
            ],
            width=radius * 0.17,
            cap="square",
        )


class HomeHeader(BoxLayout):
    """Top bar of a client's first screen: its title and the settings gear."""

    title = StringProperty()

    __events__ = ("on_settings_pressed",)

    def on_settings_pressed(self) -> None:
        pass


class TextField(HoverBehavior, TextInput):
    """A text input that shows the text cursor while the mouse is over it.

    Its look comes from the `<TextInput>` rule in `widgets.kv`.
    """

    cursor_shape = CursorShape.text


class ScreenHeader(BoxLayout):
    title = StringProperty()


Builder.load_file(str(Path(__file__).with_suffix(".kv")))
