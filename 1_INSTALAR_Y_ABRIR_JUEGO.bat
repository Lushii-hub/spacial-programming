@echo off
setlocal
title Spacial Programming - Lucia
cd /d "%~dp0"

echo ==============================================
echo  SPACIAL PROGRAMMING - PREPARACION AUTOMATICA
echo ==============================================
echo.
echo PASO 1 DE 3: Instalando o verificando Python 3.12...
py install 3.12
if errorlevel 1 goto :python_error

py -3.12 -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)" >nul 2>&1
if errorlevel 1 goto :python_error

echo.
echo PASO 2 DE 3: Preparando el entorno del juego...

if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)" >nul 2>&1
    if errorlevel 1 rmdir /s /q ".venv"
)

if not exist ".venv\Scripts\python.exe" (
    if exist ".venv" rmdir /s /q ".venv"
    py -3.12 -m venv ".venv"
)

if not exist ".venv\Scripts\python.exe" goto :environment_error

echo.
echo PASO 3 DE 3: Instalando Pygame Zero y Pygame...
".venv\Scripts\python.exe" -c "import pygame, pgzero" >nul 2>&1
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install --upgrade pip setuptools wheel
    if errorlevel 1 goto :packages_error
    ".venv\Scripts\python.exe" -m pip install -r "requirements.txt"
    if errorlevel 1 goto :packages_error
)

echo.
echo Todo esta listo. Abriendo el juego con Python 3.12...
echo.
".venv\Scripts\python.exe" "watch.py"
goto :end

:python_error
echo.
echo ERROR: No se pudo instalar Python 3.12.
echo Abre PowerShell, ejecuta: py install 3.12
echo y vuelve a abrir este archivo cuando termine.
goto :pause_error

:environment_error
echo.
echo ERROR: No se pudo crear el entorno de Python 3.12.
goto :pause_error

:packages_error
echo.
echo ERROR: No se pudieron instalar Pygame Zero y Pygame.
echo Comprueba la conexion a Internet y vuelve a intentarlo.
goto :pause_error

:pause_error
pause
exit /b 1

:end
pause
endlocal
