"""
Модуль чтения и валидации JSON-конфигурации.
"""
import json
import os
from typing import Any, Dict, List

from errors import (
    ConfigError,
    ConfigFileNotFoundError,
    ConfigParseError,
    ConfigValidationError,
)

REQUIRED_FIELDS: List[str] = [
    'package_name',
    'repository_url',
    'test_mode',
    'output_file',
]

DEFAULT_MAX_DEPTH = 5
MIN_DEPTH = 1


def _validate_string(value: Any, field: str) -> None:
    """
    Проверяет, что значение — непустая строка.
    """
    if not isinstance(value, str) or not value.strip():
        raise ConfigValidationError(
            field, "must be a non-empty string"
        )


def _validate_bool(value: Any, field: str) -> None:
    """
    Проверяет, что значение — булево.
    """
    if not isinstance(value, bool):
        raise ConfigValidationError(
            field, "must be a boolean"
        )


def _validate_positive_int(value: Any, field: str, minimum: int) -> None:
    """
    Проверяет, что значение — целое число >= minimum.
    """
    if not isinstance(value, int) or value < minimum:
        raise ConfigValidationError(
            field, f"must be >= {minimum}"
        )


def load_config(path: str) -> Dict[str, Any]:
    """
    Загружает конфигурацию из JSON-файла.
    """
    if not os.path.exists(path):
        raise ConfigFileNotFoundError(path)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ConfigParseError(path, str(e))
    except OSError as e:
        raise ConfigError(f"Cannot read file: {e}")

    return data


def validate_config(config: Dict[str, Any]) -> None:
    """
    Проверяет наличие и корректность обязательных полей.
    """
    for field in REQUIRED_FIELDS:
        if field not in config:
            raise ConfigValidationError(field, "missing")

    _validate_string(
        config.get('package_name', ''), 'package_name'
    )
    _validate_string(
        config.get('repository_url', ''), 'repository_url'
    )
    _validate_bool(
        config.get('test_mode', False), 'test_mode'
    )
    _validate_string(
        config.get('output_file', ''), 'output_file'
    )
    _validate_positive_int(
        config.get('max_depth', DEFAULT_MAX_DEPTH),
        'max_depth',
        MIN_DEPTH,
    )


def get_defaults() -> Dict[str, Any]:
    """
    Возвращает значения по умолчанию для необязательных полей.
    """
    return {
        'max_depth': DEFAULT_MAX_DEPTH,
        'filter_substring': '',
        'test_file': '',
        'version': 'latest',
    }


def prepare_config(path: str) -> Dict[str, Any]:
    """
    Загружает, валидирует и дополняет конфигурацию.
    """
    config = load_config(path)
    validate_config(config)

    defaults = get_defaults()
    for key, value in defaults.items():
        if key not in config:
            config[key] = value

    return config