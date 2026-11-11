# npm Dependency Visualizer

Инструмент визуализации графа зависимостей для npm.
Практическая работа №2, Вариант 13.

## Описание

Приложение анализирует зависимости npm-пакетов,
строит граф зависимостей и визуализирует его в формате SVG.

Реализовано чтение JSON-конфигурации с валидацией
и обработкой ошибок.

### Параметры конфигурации

- `package_name` — имя анализируемого пакета
- `repository_url` — URL npm-репозитория
- `test_mode` — режим работы с тестовым репозиторием
- `test_file` — путь к файлу тестового репозитория
- `version` — версия пакета
- `max_depth` — максимальная глубина анализа
- `filter_substring` — подстрока для фильтрации
- `output_file` — имя выходного файла с графом


## Этап 2. Сбор данных

Реализовано получение информации о зависимостях npm-пакетов
через HTTP-запросы к npm registry.

### Функции

- `fetch_package_info()` — получение данных о пакете из npm registry
- `extract_dependencies()` — извлечение списка прямых зависимостей
- `format_dependencies_list()` — форматирование вывода зависимостей

### Запуск

```bat
.\run.bat config.json
.\run.bat tests\config_valid.json
.\tests\test_config.bat
.\tests\test_fetch.bat
python src\main.py tests\config_test_simple.json
python src\main.py tests\config_test_cycle.json
python src\main.py tests\config_test_complex.json
python src\main.py config.json
4 ЭТАП
python src\main.py tests\config_test_order.json
python src\main.py tests\config_test_order_cycle.json
5 ЭТАП
python src\main.py tests\config_npm_express.json
python src\main.py tests\config_npm_react.json
python src\main.py tests\config_npm_axios.json

(POWERSHELL)
d2 tests\express.d2 tests\express.svg
d2 tests\react.d2 tests\react.svg
d2 tests\axios.d2 tests\axios.svg

start tests\express.svg
start tests\react.svg
start tests\axios.svg