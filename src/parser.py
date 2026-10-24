"""
Модуль для парсинга информации о зависимостях пакета.
"""
from typing import Any, Dict, List


def extract_dependencies(
    package_data: Dict[str, Any]
) -> List[str]:
    """
    Извлекает список прямых зависимостей из данных пакета.
    """
    dependencies = package_data.get('dependencies', {})

    if not isinstance(dependencies, dict):
        return []

    return sorted(dependencies.keys())


def format_dependencies_list(
    dependencies: List[str],
    package_name: str,
    version: str
) -> str:
    """
    Форматирует список зависимостей для вывода.
    """
    if not dependencies:
        return f"Package {package_name}@{version} has no dependencies"

    lines = [
        f"Direct dependencies for {package_name}@{version}:",
        f"Total: {len(dependencies)}",
        "",
    ]

    for dep in dependencies:
        lines.append(f"  - {dep}")

    return '\n'.join(lines)