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


def fetch_and_display(
    config: Dict[str, Any]
) -> None:
    """
    Получает и выводит зависимости пакета.

    Args:
        config: Словарь с параметрами конфигурации.
    """
    package_name = config['package_name']
    version = config['version']
    registry_url = config['repository_url']

    print(f"[FETCH] Fetching {package_name}@{version}...")

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
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <config.json>")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        config = prepare_config(config_path)
        fetch_and_display(config)
    except ConfigError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()