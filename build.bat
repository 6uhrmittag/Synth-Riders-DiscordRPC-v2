@echo off
echo === Synth Riders Discord RPC Builder ===
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or not in PATH! Please install Python 3.7 or newer.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing required dependencies...
pip install pyinstaller
pip install -r requirements.txt

echo.
echo Building application using PyInstaller...
echo.

REM Clean build directories
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo Building with console window for debugging...
python -c "content = open('main.spec', 'r').read(); content = content.replace(\"console=False\", \"console=True\"); open('main.spec', 'w').write(content)"

echo Running PyInstaller with main.spec...
pyinstaller --clean main.spec

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Build failed! See error messages above.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The executable can be found in the dist folder.
echo.

REM Display version information
if exist settings\appinfo.ini (
    for /f "tokens=2 delims==" %%a in ('findstr "AppVersion" settings\appinfo.ini') do set APP_VERSION=%%a
    echo Application version: %APP_VERSION%
    echo.
)



pause
