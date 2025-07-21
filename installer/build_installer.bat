@echo off
echo Building Synth Riders Discord RPC Installer...

REM Check if NSIS is installed
where makensis >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: NSIS (makensis) not found in PATH
    echo Please install NSIS from https://nsis.sourceforge.io/
    echo and add it to your PATH
    pause
    exit /b 1
)

REM Check if dist directory exists
if not exist "..\dist\main.exe" (
    echo ERROR: main.exe not found in dist directory
    echo Please build the application first using build.bat
    pause
    exit /b 1
)

REM Check if settings directory exists
if not exist "..\dist\settings" (
    echo ERROR: settings directory not found in dist
    echo Please ensure settings are copied during build
    pause
    exit /b 1
)

REM Get version from appinfo.ini
for /f "tokens=2 delims==" %%i in ('findstr "AppVersion" ..\dist\settings\appinfo.ini') do set VERSION=%%i
set VERSION=%VERSION: =%

echo Building installer for version %VERSION%...

REM Build the installer
makensis /DAPP_VERSION=%VERSION% setup.nsi

if %errorlevel% equ 0 (
    echo.
    echo SUCCESS: Installer created successfully!
    echo File: SynthRidersDiscordRPC-Setup-v%VERSION%.exe
    echo.
    echo Installer features:
    echo - Professional setup wizard
    echo - Automatic start menu shortcuts
    echo - Desktop shortcut
    echo - Autorun on startup
    echo - Proper uninstaller
    echo - Registry integration
    echo.
) else (
    echo ERROR: Failed to build installer
    pause
    exit /b 1
)

pause 