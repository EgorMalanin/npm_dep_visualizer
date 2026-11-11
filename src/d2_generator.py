"""
Модуль для генерации текстового представления графа на языке D2.
"""
from typing import List
from graph import DependencyGraph


def generate_d2(
    graph: DependencyGraph,
) -> str:
    """
    Генерирует D2-разметку для графа зависимостей.
    """
    lines: List[str] = []
    packages = graph.get_all_packages()

    for package in packages:
        deps = graph.get_dependencies(package)
        for dep in sorted(deps):
            lines.append(f"{package} -> {dep}")

    return '\n'.join(lines)


def save_d2_file(
    d2_content: str,
    output_path: str
) -> None:
    """
    Сохраняет D2-разметку в файл.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(d2_content)