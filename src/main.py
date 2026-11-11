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
from graph_printer import format_dependency_graph
from topo_sort import topological_sort, format_load_order
from d2_generator import generate_d2
from svg_exporter import generate_and_export
from fetcher import build_transitive_graph

MIN_ARGS_COUNT = 2
CONFIG_PATH_INDEX = 1
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def _visualize_graph(
    graph: DependencyGraph,
    package_name: str,
    output_file: str
) -> None:
    """
    Генерирует D2-разметку и сохраняет SVG.
    """
    d2_content = generate_d2(graph, package_name)

    print(f"\n[D2] Graph representation for '{package_name}':")
    print(d2_content)

    try:
        svg_path = generate_and_export(d2_content, output_file)
        print(f"\n[SVG] Saved to: {svg_path}")
    except ConfigError as e:
        print(f"\n[SVG] Warning: {e}")
        d2_path = output_file.replace('.svg', '.d2')
        from d2_generator import save_d2_file
        save_d2_file(d2_content, d2_path)
        print(f"[D2]  Saved to: {d2_path}")

def _show_load_order(
    graph: DependencyGraph,
    package_name: str
) -> None:
    """
    Выводит порядок загрузки зависимостей.
    """
    order, has_cycle = topological_sort(graph, package_name)
    print(format_load_order(order, has_cycle, package_name))

def _analyze_graph(
    graph: DependencyGraph,
    package_name: str,
    show_order: bool = False,
    visualize: bool = False,
    output_file: str = 'graph.svg'
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

    print("\nDependency graph:")
    print(format_dependency_graph(graph, package_name))

    print("\nDependency levels:")
    print(format_bfs_result(levels, has_cycle))

    if show_order:
        print()
        _show_load_order(graph, package_name)

    if visualize:
        _visualize_graph(graph, package_name, output_file)

def run_test_mode(config: Dict[str, Any]) -> None:
    """Запускает анализ в тестовом режиме."""
    test_file = config.get('test_file', '')
    package_name = config.get('package_name', 'A')
    show_order = config.get('show_load_order', False)
    visualize = config.get('visualize', False)
    output_file = config.get('output_file', 'graph.svg')

    if not test_file:
        raise ConfigError("test_file is required in test mode")

    graph = load_test_graph(test_file)
    _analyze_graph(
        graph, package_name, show_order, visualize, output_file
    )


def run_real_mode(config: Dict[str, Any]) -> None:
    """Запускает анализ в реальном режиме через npm registry."""
    package_name = config['package_name']
    version = config['version']
    registry_url = config['repository_url']
    show_order = config.get('show_load_order', False)
    visualize = config.get('visualize', False)
    output_file = config.get('output_file', 'graph.svg')
    max_depth = config.get('max_depth', 5)

    print(f"[BUILD] Building graph for {package_name}@{version}...")

    graph = build_transitive_graph(
        package_name, version, registry_url, max_depth
    )

    _analyze_graph(
        graph, package_name, show_order, visualize, output_file
    )

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