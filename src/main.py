"""
Точка входа в приложение визуализации зависимостей npm.
"""
import sys
from typing import Any, Dict

from bfs import bfs_transitive, bfs_with_levels, format_bfs_result
from config import prepare_config
from errors import ConfigError
from fetcher import build_dependency_graph
from graph import DependencyGraph
from test_loader import load_test_graph

MIN_ARGS_COUNT = 2
CONFIG_PATH_INDEX = 1
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def run_test_mode(config: Dict[str, Any]) -> None:
    """
    Запускает анализ в тестовом режиме.
    """
    test_file = config.get('test_file', '')
    package_name = config.get('package_name', 'A')

    if not test_file:
        raise ConfigError("test_file is required in test mode")

    graph = load_test_graph(test_file)
    _analyze_graph(graph, package_name)


def run_real_mode(config: Dict[str, Any]) -> None:
    """
    Запускает анализ в реальном режиме через npm registry.
    """
    package_name = config['package_name']
    version = config['version']
    registry_url = config['repository_url']

    print(f"[BUILD] Building graph for {package_name}@{version}...")

    graph = build_dependency_graph(
        package_name, version, registry_url
    )

    _analyze_graph(graph, package_name)


def _analyze_graph(
    graph: DependencyGraph,
    package_name: str
) -> None:
    """
    Анализирует граф и выводит транзитивные зависимости.
    """
    if not graph.has_package(package_name):
        print(f"Package '{package_name}' not found in graph")
        return

    deps, has_cycle = bfs_transitive(graph, package_name)
    levels = bfs_with_levels(graph, package_name)

    print(f"\nTransitive dependencies for '{package_name}':")
    print(f"Total: {len(deps)}")

    if deps:
        print("Packages: " + ', '.join(sorted(deps)))

    print("\nDependency levels:")
    print(format_bfs_result(levels, has_cycle))


def main() -> None:
    """Главная функция приложения."""
    if len(sys.argv) < MIN_ARGS_COUNT:
        print("Usage: python src/main.py <config.json>")
        sys.exit(EXIT_FAILURE)

    config_path = sys.argv[CONFIG_PATH_INDEX]

    try:
        config = prepare_config(config_path)

        if config.get('test_mode', False):
            run_test_mode(config)
        else:
            run_real_mode(config)

    except ConfigError as e:
        print(f"[ERROR] {e}")
        sys.exit(EXIT_FAILURE)


if __name__ == '__main__':
    main()