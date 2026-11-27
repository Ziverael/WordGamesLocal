from word_games.config.app import AppSettings, locate_settings_file
from word_games.config.storage import load_settings, save_settings
from word_games.ui.theme import ThemeName


def remember_theme(theme: ThemeName) -> AppSettings:
    return _remember(theme=theme)


def remember_cursor_choice(*, use_system_cursor: bool) -> AppSettings:
    return _remember(use_system_cursor=use_system_cursor)


def _remember(**changes: object) -> AppSettings:
    """Reloads first, so a change made by the other client is kept."""
    updated = load_settings().model_copy(update=changes)
    save_settings(updated, locate_settings_file())
    return updated
