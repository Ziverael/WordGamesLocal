import pytest
from kivy.uix.screenmanager import NoTransition

from word_games.ui.navigation import Navigator
from word_games.ui.screens import teacher_home as _teacher_home
from word_games.ui.screens.settings import SettingsScreen
from word_games.ui.teacher_route import TeacherRoute
from word_games.ui.widgets import GearButton


pytestmark = pytest.mark.atomic


@pytest.fixture
def navigator() -> Navigator:
    navigator = Navigator(TeacherRoute.home, transition=NoTransition())
    navigator.add_widget(
        _teacher_home.TeacherHomeScreen(name=TeacherRoute.home)
    )
    navigator.add_widget(SettingsScreen(name=TeacherRoute.settings))
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
    assert navigator.current == TeacherRoute.settings


def test_back_from_settings_returns_to_student_home(navigator):
    # given
    navigator.show(TeacherRoute.settings)

    # when
    navigator.go_back()

    # then
    assert navigator.current == TeacherRoute.home
