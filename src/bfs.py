"""
Модуль для обхода графа зависимостей алгоритмом BFS.
Итеративная реализация без рекурсии.
"""
from collections import deque
from typing import Dict, List, Set, Tuple

from graph import DependencyGraph


def bfs_transitive(
    graph: DependencyGraph,
    start: str
) -> Tuple[List[str], bool]:
    """
    Находит все транзитивные зависимости пакета через BFS.
    """
    if not graph.has_package(start):
        return [], False

    visited: Set[str] = set()
    queue: deque = deque([start])
    has_cycle = False
    result: List[str] = []

    while queue:
        current = queue.popleft()

        for dep in graph.get_dependencies(current):
            if dep in visited:
                has_cycle = True
                continue

            visited.add(dep)
            result.append(dep)
            queue.append(dep)

    return result, has_cycle


def bfs_with_levels(
    graph: DependencyGraph,
    start: str
) -> Dict[int, List[str]]:
    """
    BFS с сохранением уровня вложенности.
    """
    if not graph.has_package(start):
        return {}

    visited: Set[str] = {start}
    queue: deque = deque([(start, 0)])
    levels: Dict[int, List[str]] = {0: [start]}

    while queue:
        current, level = queue.popleft()
        next_level = level + 1

        for dep in graph.get_dependencies(current):
            if dep not in visited:
                visited.add(dep)
                if next_level not in levels:
                    levels[next_level] = []
                levels[next_level].append(dep)
                queue.append((dep, next_level))

    return levels


def format_bfs_result(
    levels: Dict[int, List[str]],
    has_cycle: bool
) -> str:
    """
    Форматирует результат BFS для вывода.
    """
    lines: List[str] = []

    for level in sorted(levels.keys()):
        packages = ', '.join(sorted(levels[level]))
        lines.append(f"Level {level}: {packages}")

    if has_cycle:
        lines.append("")
        lines.append("Warning: cyclic dependencies detected")

    return '\n'.join(lines)