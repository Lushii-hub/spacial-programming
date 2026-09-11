import os
import math
import pygame
from pgzero.rect import Rect
from pgzero.loaders import images
from config import (
    WIDTH, HEIGHT, TITLE, STUDENT_NAME,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_SCORE, COLOR_DANGER, COLOR_SUCCESS, COLOR_WHITE, COLOR_BLACK,
    FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE, FONT_SIZE_HUD, FONT_SIZE_HUD_VAL, FONT_SIZE_GAME_OVER
)

def get_font():
    if os.path.exists("fonts"):
        files = os.listdir("fonts")
        for f in files:
            if f.endswith(".ttf") or f.endswith(".otf"):
                lower_f = f.lower()
                if f != lower_f:
                    old_path = os.path.join("fonts", f)
                    new_path = os.path.join("fonts", lower_f)
                    try:
                        os.rename(old_path, new_path)
                    except Exception:
                        pass
                    f = lower_f
                return os.path.splitext(f)[0]
    return None

class UIManager:
    @staticmethod
    def draw_menu(screen, high_score=0):
        font = get_font()
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        
        screen.draw.text(TITLE, center=(center_x, center_y - 100), fontsize=FONT_SIZE_TITLE, color=COLOR_PRIMARY, owidth=2.5, ocolor=COLOR_BLACK, fontname=font)
        # La portada completa conserva la tipografía cuadriculada del juego.
        screen.draw.text(f"BY {STUDENT_NAME}", center=(center_x, center_y - 20), fontsize=FONT_SIZE_SUBTITLE, color=COLOR_WHITE, owidth=2.0, ocolor=COLOR_BLACK, fontname=font)
        screen.draw.text(f"HIGH SCORE: {high_score}", center=(center_x, center_y + 45), fontsize=22, color=COLOR_SCORE, owidth=1.5, ocolor=COLOR_BLACK, fontname=font)
        screen.draw.text("START GAME", center=(center_x, center_y + 115), fontsize=30, color=COLOR_SUCCESS, owidth=1.5, ocolor=COLOR_BLACK, fontname=font)

    @staticmethod
    def draw_character_select(screen, selected_index):
        font = get_font()
        screen.draw.text(
            "ELIGE TU PERSONAJE",
            center=(WIDTH // 2, 92),
            fontsize=36,
            color=COLOR_PRIMARY,
            owidth=2.5,
            ocolor=COLOR_BLACK,
            fontname=font,
        )

        characters = [
            ("NYAN CAT", "player/spaceship"),
            ("KIRBY", "player/kirby"),
        ]
        cards = [
            Rect((95, 155), (280, 260)),
            Rect((425, 155), (280, 260)),
        ]

        for index, ((name, image_name), card) in enumerate(zip(characters, cards)):
            border_color = COLOR_PRIMARY if index == selected_index else COLOR_WHITE
            screen.draw.filled_rect(card, (5, 10, 30))
            screen.draw.rect(card, border_color)

            character_image = images.load(image_name)
            max_width = 190
            max_height = 130
            scale = min(
                max_width / character_image.get_width(),
                max_height / character_image.get_height(),
            )
            preview_size = (
                int(character_image.get_width() * scale),
                int(character_image.get_height() * scale),
            )
            preview = pygame.transform.scale(character_image, preview_size)
            preview_x = card.centerx - preview.get_width() // 2
            preview_y = card.y + 42
            screen.surface.blit(preview, (preview_x, preview_y))

            screen.draw.text(
                name,
                center=(card.centerx, card.bottom - 45),
                fontsize=24,
                color=border_color,
                owidth=1.5,
                ocolor=COLOR_BLACK,
                fontname=font,
            )

        screen.draw.text(
            "IZQUIERDA / DERECHA PARA ELEGIR",
            center=(WIDTH // 2, 475),
            fontsize=18,
            color=COLOR_WHITE,
            fontname=font,
        )
        screen.draw.text(
            "ENTER PARA JUGAR",
            center=(WIDTH // 2, 520),
            fontsize=22,
            color=COLOR_SUCCESS,
            owidth=1.5,
            ocolor=COLOR_BLACK,
            fontname=font,
        )

    @staticmethod
    def draw_hud(screen, player, boss, hardcore_timer=0, high_score=0):
        font = get_font()
        center_x = WIDTH // 2
        margin_top = 12
        center_bar_x = center_x - 80

        screen.draw.text("SCORE", (30, margin_top), fontsize=FONT_SIZE_HUD, color=COLOR_SCORE, owidth=1, ocolor=COLOR_BLACK, fontname=font)
        screen.draw.text(f"{player.score}", (30, margin_top + 20), fontsize=FONT_SIZE_HUD_VAL, color=COLOR_PRIMARY, owidth=1.5, ocolor=COLOR_BLACK, fontname=font)
        screen.draw.text(f"RECORD: {high_score}", (30, margin_top + 51), fontsize=14, color=COLOR_WHITE, owidth=1, ocolor=COLOR_BLACK, fontname=font)

        if boss:
            screen.draw.text("BOSS >", (center_bar_x, margin_top), fontsize=FONT_SIZE_HUD, color=COLOR_DANGER, owidth=1, ocolor=COLOR_BLACK, fontname=font)
            screen.draw.rect(Rect((center_bar_x, margin_top + 24), (160, 16)), color=COLOR_WHITE)
            boss_ratio = max(0, boss.health / boss.max_health)
            screen.draw.filled_rect(Rect((center_bar_x + 2, margin_top + 26), (int(156 * boss_ratio), 12)), color=COLOR_DANGER)
        else:
            screen.draw.text("GOAL: 1000", (center_bar_x, margin_top), fontsize=FONT_SIZE_HUD, color=COLOR_PRIMARY, owidth=1, ocolor=COLOR_BLACK, fontname=font)
            screen.draw.rect(Rect((center_bar_x, margin_top + 24), (160, 16)), color=COLOR_WHITE)
            progress_ratio = min(1.0, player.score / 1000.0)
            screen.draw.filled_rect(Rect((center_bar_x + 2, margin_top + 26), (int(156 * progress_ratio), 12)), color=COLOR_SCORE)

        lives_start_x = WIDTH - 220
        screen.draw.text("LIVES", (lives_start_x, margin_top), fontsize=FONT_SIZE_HUD, color=COLOR_DANGER, owidth=1, ocolor=COLOR_BLACK, fontname=font)
        
        visible_hearts = min(max(0, player.lives), 5)

        for i in range(visible_hearts):
            screen.blit("ui/heart", (lives_start_x + i * 26, margin_top + 22))

        if hardcore_timer > 0:
            seconds = math.ceil(hardcore_timer / 60)
            screen.draw.text(f"HARDCORE {seconds}s", center=(center_x, 82), fontsize=19, color=COLOR_DANGER, owidth=1.5, ocolor=COLOR_SECONDARY, fontname=font)

    @staticmethod
    def draw_paused(screen):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 155))
        screen.surface.blit(overlay, (0, 0))

        font = get_font()
        screen.draw.text(
            "PAUSED",
            center=(WIDTH // 2, HEIGHT // 2 - 25),
            fontsize=FONT_SIZE_GAME_OVER,
            color=COLOR_PRIMARY,
            owidth=2.5,
            ocolor=COLOR_BLACK,
            fontname=font,
        )
        screen.draw.text(
            "PRESS P TO RESUME",
            center=(WIDTH // 2, HEIGHT // 2 + 25),
            fontsize=18,
            color=COLOR_WHITE,
            fontname=font,
        )

        home_button = UIManager.get_home_button()
        screen.draw.filled_rect(home_button, (5, 10, 30))
        screen.draw.rect(home_button, COLOR_PRIMARY)
        screen.draw.text(
            "GO HOME",
            center=home_button.center,
            fontsize=24,
            color=COLOR_WHITE,
            owidth=1.5,
            ocolor=COLOR_BLACK,
            fontname=font,
        )

    @staticmethod
    def get_home_button():
        return Rect((WIDTH // 2 - 105, HEIGHT // 2 + 70), (210, 52))

    @staticmethod
    def draw_game_over(screen, player, high_score=0):
        font = get_font()
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        screen.draw.text("MISSION FAILED", center=(center_x, center_y - 50), fontsize=FONT_SIZE_GAME_OVER, color=COLOR_DANGER, owidth=2.5, ocolor=COLOR_BLACK, fontname=font)
        screen.draw.text(f"Puntuacion Final: {player.score}", center=(center_x, center_y + 50), fontsize=22, color=COLOR_SECONDARY, fontname=font)
        screen.draw.text(f"Record: {high_score}", center=(center_x, center_y + 85), fontsize=20, color=COLOR_WHITE, fontname=font)

    @staticmethod
    def draw_victory(screen, player, high_score=0):
        font = get_font()
        center_x = WIDTH // 2
        center_y = HEIGHT // 2
        screen.draw.text("MISSION COMPLETE!", center=(center_x, center_y - 50), fontsize=FONT_SIZE_TITLE, color=COLOR_SUCCESS, owidth=2.5, ocolor=COLOR_BLACK, fontname=font)
        screen.draw.text(f"Puntuacion Final: {player.score}", center=(center_x, center_y + 50), fontsize=22, color=COLOR_WHITE, fontname=font)
        screen.draw.text(f"Record: {high_score}", center=(center_x, center_y + 85), fontsize=20, color=COLOR_SCORE, fontname=font)
