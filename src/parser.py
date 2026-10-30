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