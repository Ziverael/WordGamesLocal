import pytest
from kivy.uix.screenmanager import NoTransition

from word_games.ui.navigation import Navigator
from word_games.ui.screens import student_home as _student_home
from word_games.ui.screens.settings import SettingsScreen
from word_games.ui.student_route import StudentRoute
from word_games.ui.widgets import GearButton


pytestmark = pytest.mark.atomic


@pytest.fixture
def navigator() -> Navigator:
    navigator = Navigator(StudentRoute.home, transition=NoTransition())
    navigator.add_widget(
        _student_home.StudentHomeScreen(name=StudentRoute.home)
    )
    navigator.add_widget(SettingsScreen(name=StudentRoute.settings))
    return navigator


def test_gear_on_student_home_opens_settings(navigator):
    # given
    gear = next(
        widget
        for widget in navigator.current_screen.walk()
        if isinstance(widget, GearButton)
    )

    # when
    gear.dispatch("on_release")

    # then
    assert navigator.current == StudentRoute.settings


def test_back_from_settings_returns_to_student_home(navigator):
    # given
    navigator.show(StudentRoute.settings)

    # when
    navigator.go_back()

    # then
    assert navigator.current == StudentRoute.home
