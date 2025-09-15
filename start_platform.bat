@echo off
echo Starting Enhanced Health AI Platform...
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing/updating requirements...
pip install -r requirements.txt

echo.
echo Training ML models (if needed)...
python train_models.py --all

echo.
echo Starting the platform...
python start_platform.py

pause
