"""
Точка входа в приложение визуализации зависимостей npm.
"""
import sys
from typing import Any, Dict

from config import prepare_config
from errors import ConfigError
from fetcher import fetch_package_info
from parser import (
    extract_dependencies,
    format_dependencies_list,
)

MIN_ARGS_COUNT = 2
CONFIG_PATH_INDEX = 1
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def print_parameters(config: Dict[str, Any]) -> None:
    """
    Выводит все параметры конфигурации.
    """
    print("[CONFIG] Loaded parameters:")
    for key, value in config.items():
        print(f"  {key} = {value}")


def fetch_and_display(
    config: Dict[str, Any]
) -> None:
    """
    Получает и выводит зависимости пакета.
    """
    package_name = config['package_name']
    version = config['version']
    registry_url = config['repository_url']

    print(f"\n[FETCH] Fetching {package_name}@{version}...")

    package_data = fetch_package_info(
        package_name, version, registry_url
    )

    dependencies = extract_dependencies(package_data)
    output = format_dependencies_list(
        dependencies, package_name, version
    )

    print(output)


def main() -> None:
    """Главная функция приложения."""
    if len(sys.argv) < MIN_ARGS_COUNT:
        print("Usage: python src/main.py <config.json>")
        sys.exit(EXIT_FAILURE)

    config_path = sys.argv[CONFIG_PATH_INDEX]

    try:
        config = prepare_config(config_path)
        print_parameters(config)
        fetch_and_display(config)
    except ConfigError as e:
        print(f"[ERROR] {e}")
        sys.exit(EXIT_FAILURE)


if __name__ == '__main__':
    main()