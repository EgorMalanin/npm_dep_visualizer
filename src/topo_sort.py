"""
Модуль топологической сортировки графа зависимостей.
Реализует алгоритм Кана (итеративный BFS-подход).
"""
from collections import deque
from typing import Dict, List, Tuple

from graph import DependencyGraph

ZERO_INDEGREE = 0


def topological_sort(
    graph: DependencyGraph,
    start: str
) -> Tuple[List[str], bool]:
    """
    Выполняет топологическую сортировку подграфа от start.
    Алгоритм Кана: итеративный BFS по узлам с нулевой
    входящей степенью.
    """
    if not graph.has_package(start):
        return [], False
    subgraph = _build_subgraph(graph, start)
    indegrees = _compute_indegrees_for_subgraph(
        graph, subgraph
    )
    queue: deque = deque()
    for pkg in sorted(subgraph):
        if indegrees[pkg] == ZERO_INDEGREE:
            queue.append(pkg)
    order: List[str] = []
    has_cycle = False
    while queue:
        current = queue.popleft()
        order.append(current)
        for dep in sorted(graph.get_dependencies(current)):
            if dep not in subgraph:
                continue
            indegrees[dep] -= 1
            if indegrees[dep] == ZERO_INDEGREE:
                queue.append(dep)
    if len(order) != len(subgraph):
        has_cycle = True

    return order, has_cycle


def _build_subgraph(
    graph: DependencyGraph,
    start: str
) -> set:
    """
    Строит множество пакетов, достижимых из start.
    """
    visited: set = {start}
    queue: deque = deque([start])

    while queue:
        current = queue.popleft()
        for dep in graph.get_dependencies(current):
            if dep not in visited:
                visited.add(dep)
                queue.append(dep)

    return visited


def _compute_indegrees_for_subgraph(
    graph: DependencyGraph,
    subgraph: set
) -> Dict[str, int]:
    """
    Вычисляет входящие степени только для узлов подграфа.
    """
    indegrees: Dict[str, int] = {pkg: 0 for pkg in subgraph}

    for pkg in subgraph:
        for dep in graph.get_dependencies(pkg):
            if dep in subgraph:
                indegrees[dep] += 1

    return indegrees


def format_load_order(
    order: List[str],
    has_cycle: bool,
    package_name: str
) -> str:
    """
    Форматирует порядок загрузки для вывода.
    """
    lines: List[str] = []
    lines.append(f"Load order for '{package_name}':")

    if not order:
        lines.append("  (no packages)")
        return '\n'.join(lines)

    install_order = list(reversed(order))

    for index, pkg in enumerate(install_order, 1):
        marker = " <-- root" if pkg == package_name else ""
        lines.append(f"  {index}. {pkg}{marker}")

    if has_cycle:
        lines.append("")
        lines.append(
            "Warning: cyclic dependencies detected, "
            "order may be incomplete"
        )

    return '\n'.join(lines)