"""Student client: import an assignment file and play it.

This module must never import teacher-only code. PyInstaller bundles
whatever is reachable from here, so an import of the editor would ship
the authoring screens to students.
"""

from kivy.app import App
from kivy.uix.label import Label


class StudentApp(App):
    title = "Word Games - Student"

    def build(self) -> Label:
        return Label(text=self.title)


def run() -> None:
    StudentApp().run()


if __name__ == "__main__":
    run()
