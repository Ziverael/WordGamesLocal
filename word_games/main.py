from kivy.app import App
from kivy.uix.label import Label


class WordGamesApp(App):
    title = "Word Games"

    def build(self) -> Label:
        return Label(text="Word Games")


def run() -> None:
    WordGamesApp().run()
