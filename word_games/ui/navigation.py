from kivy.uix.screenmanager import ScreenManager


class Navigator(ScreenManager):
    """Remembers the screens visited, so every screen can go back.

    `current` is the Kivy property of ScreenManager. It is annotated here
    only because Kivy ships no type hints.
    """

    current: str

    def __init__(self, main_menu_screen: str, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.main_menu_screen = main_menu_screen
        self._visited: list[str] = []

    def show(self, screen_name: str) -> None:
        self._visited.append(self.current)
        self.transition.direction = "left"
        self.current = screen_name

    def go_back(self) -> None:
        if not self._visited:
            return
        self.transition.direction = "right"
        self.current = self._visited.pop()

    def is_main_menu(self) -> bool:
        return self.current == self.main_menu_screen
