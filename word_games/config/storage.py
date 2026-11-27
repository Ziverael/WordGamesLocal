import logging
import tomllib
from pathlib import Path
from typing import Final

import tomli_w
from pydantic import ValidationError

from word_games.config.app import AppSettings
from word_games.io_ import write_text_atomically


_logger: Final = logging.getLogger(__name__)


def load_settings() -> AppSettings:
    """A damaged settings file must not stop the app from starting."""
    try:
        return AppSettings()
    except (tomllib.TOMLDecodeError, ValidationError, OSError):
        _logger.warning(
            "Ignoring unreadable settings, using defaults.", exc_info=True
        )
        return AppSettings.model_construct()


def save_settings(settings: AppSettings, path: Path) -> None:
    write_text_atomically(
        tomli_w.dumps(settings.model_dump(mode="json")),
        path,
    )
