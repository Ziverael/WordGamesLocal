import pytest
from kivy.uix.screenmanager import NoTransition, Screen

from word_games.ui import navigation as _navigation


pytestmark = pytest.mark.atomic


@pytest.fixture
def navigator() -> _navigation.Navigator:
    navigator = _navigation.Navigator(
        main_menu_screen="home", transition=NoTransition()
    )
    for name in ("home", "types", "editor"):
        navigator.add_widget(Screen(name=name))
    return navigator


def test_first_screen_is_shown_initially(navigator):
    # then
    assert navigator.current == "home"


def test_go_back_returns_through_every_visited_screen(navigator):
    # given
    navigator.show("types")
    navigator.show("editor")

    # when
    navigator.go_back()
    first_step = navigator.current
    navigator.go_back()
    second_step = navigator.current

    # then
    assert (first_step, second_step) == ("types", "home")


def test_go_back_on_first_screen_stays_there(navigator):
    # when
    navigator.go_back()

    # then
    assert navigator.current == "home"
