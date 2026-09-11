import os
import shutil
import subprocess
import sys


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENV_DIR = os.path.join(PROJECT_DIR, ".venv")

if os.name == "nt":
    VENV_PYTHON = os.path.join(VENV_DIR, "Scripts", "python.exe")
else:
    VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")


def run(command):
    try:
        return subprocess.run(command, cwd=PROJECT_DIR).returncode
    except OSError:
        return 1


def valid_environment():
    if not os.path.exists(VENV_PYTHON):
        return False

    check = [
        VENV_PYTHON,
        "-c",
        "import sys; raise SystemExit(0 if sys.version_info[:2] == (3, 12) else 1)",
    ]
    return run(check) == 0


def find_python_312():
    if os.name == "nt":
        if run(["py", "-3.12", "-c", "import sys"]) != 0:
            print("Instalando Python 3.12...")
            if run(["py", "install", "3.12"]) != 0:
                return None
        return ["py", "-3.12"]

    python_312 = shutil.which("python3.12")
    if python_312:
        return [python_312]
    if sys.version_info[:2] == (3, 12):
        return [sys.executable]
    return None


def prepare_game():
    if not valid_environment():
        python_312 = find_python_312()
        if not python_312:
            print("No se pudo encontrar Python 3.12.")
            return False

        if os.path.isdir(VENV_DIR):
            shutil.rmtree(VENV_DIR)

        print("Creando el entorno del juego...")
        if run(python_312 + ["-m", "venv", VENV_DIR]) != 0:
            return False

    package_check = [VENV_PYTHON, "-c", "import pygame, pgzero"]
    if run(package_check) != 0:
        print("Instalando Pygame Zero y Pygame...")
        requirements = os.path.join(PROJECT_DIR, "requirements.txt")
        if run([VENV_PYTHON, "-m", "pip", "install", "-r", requirements]) != 0:
            return False

    return True


def main():
    if prepare_game():
        print("Todo listo. Abriendo Cosmic Adventure...")
        watch_file = os.path.join(PROJECT_DIR, "watch.py")
        return subprocess.call([VENV_PYTHON, watch_file], cwd=PROJECT_DIR)

    print("No fue posible preparar el juego. Revisa la conexión a Internet.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
