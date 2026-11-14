from kivy.app import App
from kivy.uix.label import Label


class TeacherApp(App):
    title = "Word Games - Teacher"

    def build(self) -> Label:
        return Label(text=self.title)


def run() -> None:
    TeacherApp().run()


if __name__ == "__main__":
    run()
