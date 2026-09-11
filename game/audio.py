"""Música y efectos de sonido del juego."""

import math
import os

import pygame


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOUND_DIR = os.path.join(PROJECT_DIR, "sonido")
sound_cache = {}

SOUND_CHANNELS = {
    "launch": (0,),
    "nyan_shoot": (0,),
    "impact": (1, 8, 9),
    "boss_shoot": (2,),
    "hardcore_start": (3,),
    "defeat": (4,),
    "galaxy_brain": (5,),
    "harry_maguire": (6,),
    "kirby_shoot": (10,),
}

# Los disparos rápidos no deben iniciar varias copias del mismo efecto.
NON_OVERLAPPING_SOUNDS = {"nyan_shoot", "kirby_shoot"}


def find_sound(name):
    for extension in (".wav", ".ogg", ".mp3"):
        path = os.path.join(SOUND_DIR, name + extension)
        if os.path.exists(path):
            return path
    return None


def get_sound(name):
    if name not in sound_cache:
        path = find_sound(name)
        if path:
            sound_cache[name] = pygame.mixer.Sound(path)
    return sound_cache.get(name)


def play(sound_name):
    """Reproduce cada efecto completo, sin limitar su duración."""
    try:
        pygame.mixer.set_num_channels(24)
        sound = get_sound(sound_name)
        if sound:
            # La canción final conserva la reproducción original de la versión 14.
            if sound_name == "harry_maguire":
                sound.play()
                return

            channel_numbers = SOUND_CHANNELS.get(sound_name, (23,))
            if sound_name in NON_OVERLAPPING_SOUNDS:
                channel = pygame.mixer.Channel(channel_numbers[0])
                if channel.get_busy():
                    return
                channel.play(sound)
                return

            channel = next(
                (
                    pygame.mixer.Channel(number)
                    for number in channel_numbers
                    if not pygame.mixer.Channel(number).get_busy()
                ),
                pygame.mixer.Channel(channel_numbers[0]),
            )
            channel.play(sound)
    except Exception:
        pass


def sound_duration_frames(sound_name, fps=60):
    """Devuelve la duración real del sonido expresada en cuadros."""
    try:
        sound = get_sound(sound_name)
        if sound:
            return math.ceil(sound.get_length() * fps)
    except Exception:
        pass
    return 0


def effect_is_playing(sound_name):
    try:
        return any(
            pygame.mixer.Channel(number).get_busy()
            for number in SOUND_CHANNELS.get(sound_name, ())
        )
    except Exception:
        return False


def fadeout_effect(sound_name, milliseconds=500):
    try:
        if sound_name == "harry_maguire":
            sound = get_sound(sound_name)
            if sound:
                sound.fadeout(milliseconds)
            return

        for channel_number in SOUND_CHANNELS.get(sound_name, ()):
            pygame.mixer.Channel(channel_number).fadeout(milliseconds)
    except Exception:
        pass


def stop_gameplay_effects():
    try:
        for sound_name in (
            "launch",
            "nyan_shoot",
            "kirby_shoot",
            "impact",
            "boss_shoot",
            "hardcore_start",
        ):
            for channel_number in SOUND_CHANNELS[sound_name]:
                pygame.mixer.Channel(channel_number).stop()
    except Exception:
        pass


def pause_all_audio():
    try:
        pygame.mixer.pause()
        pygame.mixer.music.pause()
    except Exception:
        pass


def resume_all_audio():
    try:
        pygame.mixer.unpause()
        pygame.mixer.music.unpause()
    except Exception:
        pass


def start_music(track_name, volume=0.55):
    try:
        path = find_sound(track_name)
        if path:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
    except Exception:
        pass


def set_music_volume(volume):
    try:
        pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    except Exception:
        pass


def fadeout_music(seconds=1.5):
    try:
        pygame.mixer.music.fadeout(int(seconds * 1000))
    except Exception:
        pass


def stop_music():
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
