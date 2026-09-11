"""Guarda el récord de Cosmic Adventure."""

import os
from pathlib import Path


def get_record_file():
    app_data = os.getenv("APPDATA")
    if app_data:
        folder = Path(app_data) / "CosmicAdventureLucia"
    else:
        folder = Path.home() / ".cosmic_adventure_lucia"
    return folder / "record.txt"


def load_record():
    try:
        return max(0, int(get_record_file().read_text(encoding="utf-8").strip()))
    except (OSError, ValueError):
        return 0


def save_record(score):
    score = max(0, int(score))
    try:
        record_file = get_record_file()
        record_file.parent.mkdir(parents=True, exist_ok=True)
        record_file.write_text(str(score), encoding="utf-8")
    except OSError:
        pass
    return score
