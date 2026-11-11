"""
Модуль для получения данных из npm registry.
Использует только стандартные библиотеки Python.
"""
import json
import urllib.error
import urllib.request
from collections import deque
from typing import Any, Dict, List, NamedTuple

from errors import ConfigError
from graph import DependencyGraph

NPM_REGISTRY_URL = 'https://registry.npmjs.org/'
TIMEOUT_SECONDS = 10


class _BfsContext(NamedTuple):
    """Контекст для BFS-обхода графа зависимостей."""
    max_depth: int
    registry_url: str
    graph: DependencyGraph
    visited: set
    queue: deque


def fetch_package_info(
    package_name: str,
    version: str,
    registry_url: str = NPM_REGISTRY_URL
) -> Dict[str, Any]:
    """
    Получает информацию о пакете из npm registry.
    """
    url = f"{registry_url}{package_name}/{version}"

    try:
        request = urllib.request.Request(url)
        request.add_header('Accept', 'application/json')

        with urllib.request.urlopen(
            request, timeout=TIMEOUT_SECONDS
        ) as response:
            raw_data = response.read()

    except urllib.error.HTTPError as e:
        raise ConfigError(
            f"HTTP error {e.code} for {package_name}@{version}"
        )
    except urllib.error.URLError as e:
        raise ConfigError(
            f"Network error: {e.reason}"
        )
    except TimeoutError:
        raise ConfigError(
            f"Timeout while fetching {package_name}@{version}"
        )
    try:
        return json.loads(raw_data.decode('utf-8'))
    except json.JSONDecodeError as e:
        raise ConfigError(
            f"Invalid JSON response: {e}"
        )


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


def build_dependency_graph(
    package_name: str,
    version: str,
    registry_url: str = NPM_REGISTRY_URL
) -> DependencyGraph:
    """
    Строит граф только прямых зависимостей пакета.
    """
    package_data = fetch_package_info(
        package_name, version, registry_url
    )

    graph = DependencyGraph()
    graph.add_package(package_name)

    deps = extract_dependencies(package_data)
    for dep in deps:
        graph.add_dependency(package_name, dep)

    return graph


def _fetch_with_fallback(
    package_name: str,
    version: str,
    registry_url: str
) -> Dict[str, Any]:
    """
    Получает данные пакета с fallback на версию 'latest'.
    """
    try:
        return fetch_package_info(
            package_name, version, registry_url
        )
    except ConfigError:
        return fetch_package_info(
            package_name, 'latest', registry_url
        )


def _process_package(
    current_pkg: str,
    current_ver: str,
    depth: int,
    ctx: _BfsContext
) -> None:
    """
    Обрабатывает один пакет: добавляет зависимости в граф.
    """
    if depth >= ctx.max_depth:
        return

    try:
        pkg_data = _fetch_with_fallback(
            current_pkg, current_ver, ctx.registry_url
        )
        deps_dict = pkg_data.get('dependencies', {})

        if not isinstance(deps_dict, dict):
            return

        for dep_name, dep_ver in deps_dict.items():
            ctx.graph.add_dependency(current_pkg, dep_name)
            if dep_name not in ctx.visited:
                ctx.queue.append(
                    (dep_name, dep_ver, depth + 1)
                )

    except ConfigError:
        pass


def build_transitive_graph(
    package_name: str,
    version: str,
    registry_url: str = NPM_REGISTRY_URL,
    max_depth: int = 5
) -> DependencyGraph:
    """
    Строит транзитивный граф зависимостей пакета.
    """
    graph = DependencyGraph()
    visited: set = set()
    queue: deque = deque([(package_name, version, 0)])

    ctx = _BfsContext(
        max_depth=max_depth,
        registry_url=registry_url,
        graph=graph,
        visited=visited,
        queue=queue,
    )

    while queue:
        current_pkg, current_ver, depth = queue.popleft()

        if current_pkg in visited:
            continue

        visited.add(current_pkg)
        graph.add_package(current_pkg)

        _process_package(
            current_pkg, current_ver, depth, ctx
        )

    return graph