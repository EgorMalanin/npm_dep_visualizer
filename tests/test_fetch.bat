@echo off
echo === Test 1: Fetch express dependencies ===
python src\main.py config.json

echo.
echo === Test 2: Fetch react dependencies ===
python src\main.py tests\config_valid.json

echo.
echo === Test 3: Invalid package name ===
python src\main.py tests\config_invalid.json