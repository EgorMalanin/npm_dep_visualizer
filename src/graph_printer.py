"""
Модуль для вывода графа зависимостей в текстовом формате.
"""
from typing import List
from graph import DependencyGraph


def format_dependency_graph(
    graph: DependencyGraph,
    root_package: str
) -> str:
    """
    Форматирует граф зависимостей в виде ПАКЕТ -> ЗАВ1, ЗАВ2.
    """
    lines: List[str] = []

    packages = graph.get_all_packages()

    for package in packages:
        deps = graph.get_dependencies(package)

        if deps:
            deps_str = ', '.join(sorted(deps))
            lines.append(f"{package} -> {deps_str}")
        else:
            lines.append(f"{package} -> нет")

    return '\n'.join(lines)