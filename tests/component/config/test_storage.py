from pathlib import Path

import pytest
from pytest_mock import MockerFixture

from word_games.config import app as _app
from word_games.config import controller as _controller
from word_games.config import storage as _storage
from word_games.config.app import AppSettings, Language
from word_games.ui.theme import DEFAULT_THEME, ThemeName


pytestmark = pytest.mark.atomic


@pytest.fixture
def settings_file(
    tmp_path, mocker: MockerFixture, monkeypatch: pytest.MonkeyPatch
) -> Path:
    path = tmp_path / "word-games" / "settings.toml"
    for module in (_app, _controller):
        mocker.patch.object(module, "locate_settings_file", return_value=path)
    for variable in (
        "WORD_GAMES_THEME",
        "WORD_GAMES_LANGUAGE",
        "WORD_GAMES_USE_SYSTEM_CURSOR",
    ):
        monkeypatch.delenv(variable, raising=False)
    return path


def test_missing_file_gives_defaults(settings_file):
    # when
    settings = _storage.load_settings()

    # then
    assert settings == AppSettings(theme=DEFAULT_THEME, language=Language.en)


def test_saved_settings_load_back(settings_file):
    # given
    saved = AppSettings(theme=ThemeName.vibrant_tones)
    _storage.save_settings(saved, settings_file)

    # when
    loaded = _storage.load_settings()

    # then
    assert loaded == saved


def test_saved_file_is_readable_toml(settings_file):
    # given
    _storage.save_settings(
        AppSettings(theme=ThemeName.cherry_blossom), settings_file
    )

    # when
    content = settings_file.read_text()

    # then
    assert content == (
        'theme = "cherry_blossom"\nlanguage = "en"\nuse_system_cursor = false\n'
    )


def test_environment_variable_overrides_the_file(
    settings_file, monkeypatch: pytest.MonkeyPatch
):
    # given
    _storage.save_settings(
        AppSettings(theme=ThemeName.summer_fun), settings_file
    )
    monkeypatch.setenv("WORD_GAMES_THEME", "cherry_blossom")

    # when
    settings = _storage.load_settings()

    # then
    assert settings.theme == ThemeName.cherry_blossom


@pytest.mark.controller
def test_remembered_theme_is_loaded_on_next_start(settings_file):
    # given
    _controller.remember_theme(ThemeName.vibrant_tones)

    # when
    settings = _storage.load_settings()

    # then
    assert settings.theme == ThemeName.vibrant_tones


@pytest.mark.controller
def test_remembered_cursor_choice_keeps_the_theme(settings_file):
    # given
    _controller.remember_theme(ThemeName.cherry_blossom)

    # when
    _controller.remember_cursor_choice(use_system_cursor=True)
    settings = _storage.load_settings()

    # then
    assert (settings.theme, settings.use_system_cursor) == (
        ThemeName.cherry_blossom,
        True,
    )


@pytest.mark.parametrize(
    "file_content",
    [
        pytest.param(
            'theme = "cherry_blossom"\n    language = en"\nuse_system_cursor = false\n',
            id="broken TOML syntax",
        ),
        pytest.param(
            'theme = "invalid_theme"\nlanguage = "en"\nuse_system_cursor = false\n',
            id="unknown theme",
        ),
        pytest.param(
            'theme = 1\nlanguage = "en"\nuse_system_cursor = false\n',
            id="theme wrong type",
        ),
    ],
)
def test_invalid_file(
    settings_file, caplog: pytest.LogCaptureFixture, file_content: str
):
    # given
    settings_file.parent.mkdir(parents=True, exist_ok=True)
    settings_file.write_text(file_content)

    # when
    settings = _storage.load_settings()

    # then
    assert (
        settings.theme,
        settings.language,
        settings.use_system_cursor,
        "Ignoring unreadable settings" in caplog.text,
    ) == (DEFAULT_THEME, Language.en, False, True)
