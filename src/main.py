"""
Точка входа в приложение визуализации зависимостей npm.
"""
import sys
from typing import Any, Dict

from config import prepare_config
from errors import ConfigError

MIN_ARGS_COUNT = 2
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def print_parameters(config: Dict[str, Any]) -> None:
    """
    Выводит все параметры конфигурации в формате ключ-значение.
    """
    print("[CONFIG] Loaded parameters:")
    for key, value in config.items():
        print(f"  {key} = {value}")


def main() -> None:
    """Главная функция приложения."""
    if len(sys.argv) < MIN_ARGS_COUNT:
        print("Usage: python src/main.py <config.json>")
        sys.exit(EXIT_FAILURE)

    config_path = sys.argv[1]

    try:
        config = prepare_config(config_path)
        print_parameters(config)
    except ConfigError as e:
        print(f"[ERROR] {e}")
        sys.exit(EXIT_FAILURE)


if __name__ == '__main__':
    main()