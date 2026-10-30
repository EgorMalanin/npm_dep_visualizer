"""
Модуль для представления графа зависимостей пакетов.
"""
from typing import Dict, List, Set


class DependencyGraph:
    """Граф зависимостей пакетов."""

    def __init__(self) -> None:
        """Инициализирует пустой граф."""
        self._edges: Dict[str, List[str]] = {}

    def add_package(self, package: str) -> None:
        """
        Добавляет пакет в граф без зависимостей.
        """
        if package not in self._edges:
            self._edges[package] = []

    def add_dependency(
        self, package: str, dependency: str
    ) -> None:
        """
        Добавляет зависимость package -> dependency.
        """
        self.add_package(package)
        self.add_package(dependency)
        if dependency not in self._edges[package]:
            self._edges[package].append(dependency)

    def get_dependencies(
        self, package: str
    ) -> List[str]:
        """
        Возвращает прямые зависимости пакета.
        """
        return list(self._edges.get(package, []))

    def get_all_packages(self) -> List[str]:
        """
        Возвращает все пакеты в графе.
        """
        return sorted(self._edges.keys())

    def has_package(self, package: str) -> bool:
        """
        Проверяет наличие пакета в графе.
        """
        return package in self._edges