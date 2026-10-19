"""
Модуль пользовательских исключений для валидации конфигурации.
"""


class ConfigError(Exception):
    """Базовое исключение для ошибок конфигурации."""

    def __init__(self, message: str) -> None:
        """
        Инициализирует исключение конфигурации.
        """
        super().__init__(message)
        self.message = message


class ConfigFileNotFoundError(ConfigError):
    """Файл конфигурации не найден."""

    def __init__(self, path: str) -> None:
        """
        Инициализирует исключение отсутствия файла.
        """
        super().__init__(f"Config file not found: {path}")


class ConfigParseError(ConfigError):
    """Ошибка парсинга JSON-файла."""

    def __init__(self, path: str, reason: str) -> None:
        """
        Инициализирует исключение парсинга.
        """
        super().__init__(
            f"Failed to parse config '{path}': {reason}"
        )


class ConfigValidationError(ConfigError):
    """Ошибка валидации полей конфигурации."""

    def __init__(self, field: str, reason: str) -> None:
        """
        Инициализирует исключение валидации.
        """
        super().__init__(
            f"Invalid config field '{field}': {reason}"
        )