@echo off
echo === Test 1: Valid config ===
python src\main.py tests\config_valid.json

echo.
echo === Test 2: Invalid config ===
python src\main.py tests\config_invalid.json

echo.
echo === Test 3: Missing fields ===
python src\main.py tests\config_missing.json

echo.
echo === Test 4: Non-existent file ===
python src\main.py tests\nonexistent.json

echo.
echo === Test 5: No arguments config ===
python src\main.py

echo.
echo === Test 6: Default config ===
python src\main.py config.json