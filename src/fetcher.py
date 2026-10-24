"""
Модуль для получения данных из npm registry.
Использует только стандартные библиотеки Python.
"""
import json
import urllib.error
import urllib.request
from typing import Any, Dict
from errors import ConfigError


NPM_REGISTRY_URL = 'https://registry.npmjs.org/'
TIMEOUT_SECONDS = 10


def fetch_package_info(package_name: str,version: str,
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