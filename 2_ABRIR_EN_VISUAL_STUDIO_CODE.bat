@echo off
setlocal
title Cosmic Adventure - Visual Studio Code
cd /d "%~dp0"

set "WORKSPACE=%~dp0Cosmic_Adventure.code-workspace"
set "README_FILE=%~dp0README.md"

where code >nul 2>&1
if not errorlevel 1 (
    code --reuse-window "%WORKSPACE%" "%README_FILE%"
    exit /b 0
)

if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" (
    start "" "%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe" --reuse-window "%WORKSPACE%" "%README_FILE%"
    exit /b 0
)

if exist "%ProgramFiles%\Microsoft VS Code\Code.exe" (
    start "" "%ProgramFiles%\Microsoft VS Code\Code.exe" --reuse-window "%WORKSPACE%" "%README_FILE%"
    exit /b 0
)

echo No se encontro Visual Studio Code en esta computadora.
echo Descargalo desde: https://code.visualstudio.com/
echo Durante la instalacion selecciona la opcion para agregar Code al PATH.
pause
exit /b 1
