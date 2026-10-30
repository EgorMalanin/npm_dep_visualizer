"""
Модуль для получения данных из npm registry.
Использует только стандартные библиотеки Python.
"""
import json
import urllib.error
import urllib.request
from typing import Any, Dict, List

from errors import ConfigError
from graph import DependencyGraph

NPM_REGISTRY_URL = 'https://registry.npmjs.org/'
TIMEOUT_SECONDS = 10


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
    Строит граф прямых зависимостей пакета.
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