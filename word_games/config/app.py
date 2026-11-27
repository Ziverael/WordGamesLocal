from enum import StrEnum, auto
from pathlib import Path
from typing import Final

from platformdirs import user_config_path
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

from word_games.ui.theme import DEFAULT_THEME, ThemeName


APP_DIRECTORY_NAME: Final = "word-games"
SETTINGS_FILE_NAME: Final = "settings.toml"


class Language(StrEnum):
    en = auto()


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="WORD_GAMES_", extra="ignore", frozen=True
    )

    theme: ThemeName = DEFAULT_THEME
    language: Language = Language.en
    use_system_cursor: bool = False

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,  # noqa: ARG003
        file_secret_settings: PydanticBaseSettingsSource,  # noqa: ARG003
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            TomlConfigSettingsSource(
                settings_cls, toml_file=locate_settings_file()
            ),
        )


def locate_settings_file() -> Path:
    """~/.config on Linux, AppData on Windows, Application Support on macOS."""
    return (
        user_config_path(APP_DIRECTORY_NAME, appauthor=False)
        / SETTINGS_FILE_NAME
    )
