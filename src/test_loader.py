"""
Модуль для загрузки графа зависимостей из тестового файла.
Формат файла: PACKAGE: DEP1, DEP2, DEP3
"""
import os
from typing import List

from errors import ConfigError
from graph import DependencyGraph


def load_test_graph(path: str) -> DependencyGraph:
    """
    Загружает граф зависимостей из текстового файла.
    """
    if not os.path.exists(path):
        raise ConfigError(f"Test file not found: {path}")

    graph = DependencyGraph()

    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                _parse_line(line, line_num, graph)
    except OSError as e:
        raise ConfigError(f"Cannot read test file: {e}")

    return graph


def _parse_line(
    line: str,
    line_num: int,
    graph: DependencyGraph
) -> None:
    """
    Парсит одну строку файла и добавляет зависимости в граф.
    """
    stripped = line.strip()

    if not stripped or stripped.startswith('#'):
        return

    if ':' not in stripped:
        raise ConfigError(
            f"Invalid format at line {line_num}: {stripped}"
        )

    package, deps_str = stripped.split(':', 1)
    package = package.strip()

    if not package:
        raise ConfigError(
            f"Empty package name at line {line_num}"
        )

    graph.add_package(package)

    deps_list: List[str] = _parse_deps(deps_str)

    for dep in deps_list:
        graph.add_dependency(package, dep)


def _parse_deps(deps_str: str) -> List[str]:
    """
    Парсит строку зависимостей в список имён.
    """
    if not deps_str.strip():
        return []

    return [
        dep.strip()
        for dep in deps_str.split(',')
        if dep.strip()
    ]