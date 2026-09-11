import random

from config import HEIGHT, WIDTH
from game.audio import (
    fadeout_effect,
    fadeout_music,
    pause_all_audio,
    play,
    resume_all_audio,
    set_music_volume,
    start_music,
    stop_gameplay_effects,
    stop_music,
)
from game.background import BackgroundManager
from game.boss import Boss
from game.collisions import CollisionManager
from game.player import Player
from game.powerup import HardcoreCan
from game.record import load_record, save_record
from game.ui import UIManager
from game.victory import VictorySequence
from game.waves import WaveManager


class GameManager:
    CHARACTERS = ("nyan", "kirby")

    def __init__(self):
        self.state = "MENU"
        self.background = BackgroundManager()
        self.waves = WaveManager()

        self.player = None
        self.boss = None
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.victory_sequence = None
        self.boss_music_fading = False
        self.selected_character_index = 0
        self.high_score = load_record()

        # Único extra del juego: la lata RUN FAST.
        self.hardcore_can = None
        self.hardcore_can_timer = 120
        self.hardcore_timer = 0
        self.hardcore_duration = 45 * 60

    @property
    def hardcore_active(self):
        return self.hardcore_timer > 0

    def start_game(self):
        character = self.CHARACTERS[self.selected_character_index]
        self.player = Player(character)
        self.boss = None
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.explosions = []
        self.victory_sequence = None
        self.boss_music_fading = False
        self.waves = WaveManager()
        self.hardcore_can = None
        self.hardcore_can_timer = 120
        self.hardcore_timer = 0
        self.state = "PLAYING"
        start_music(self.player.music_name, 0.55)

    def update_record(self):
        if self.player and self.player.score > self.high_score:
            self.high_score = save_record(self.player.score)

    def activate_hardcore(self):
        self.hardcore_can = None
        self.hardcore_timer = self.hardcore_duration
        play("hardcore_start")
        start_music(self.player.hardcore_music_name, 0.70)

    def finish_hardcore(self):
        self.hardcore_timer = 0
        if self.boss:
            stop_music()
        else:
            start_music(self.player.music_name, 0.55)
            self.update_background_music()

    def update_hardcore_can(self):
        if self.boss:
            self.hardcore_can = None
            return

        if self.hardcore_active:
            return

        if self.hardcore_can:
            self.hardcore_can.move()
            if self.hardcore_can.actor.colliderect(self.player.actor):
                self.activate_hardcore()
            elif self.hardcore_can.is_off_screen():
                self.hardcore_can = None
                self.hardcore_can_timer = 0
            return

        self.hardcore_can_timer += 1
        if self.hardcore_can_timer >= 270:
            self.hardcore_can_timer = 0
            y = random.randint(100, HEIGHT - 100)
            self.hardcore_can = HardcoreCan(WIDTH + 40, y)

    def start_victory_sequence(self):
        """Inicia el meme antes de mostrar el resultado final."""
        if self.state != "PLAYING":
            return

        self.state = "VICTORY_MEME"
        self.victory_sequence = VictorySequence()
        stop_music()
        play("galaxy_brain")

    def update_victory_sequence(self):
        self.victory_sequence.update()

        if self.victory_sequence.should_announce_victory():
            fadeout_effect("galaxy_brain", 700)
            play("harry_maguire")

        if self.victory_sequence.finished:
            self.state = "VICTORY"

    def update_background_music(self):
        """Baja la música conforme la puntuación se acerca al jefe final."""
        if self.boss:
            if not self.boss_music_fading:
                self.boss_music_fading = True
                fadeout_music(1.2)
            return

        progress = min(1.0, max(0.0, self.player.score / 1000.0))
        base_volume = 0.70 if self.hardcore_active else 0.55
        set_music_volume(base_volume * (1.0 - progress))

    def update(self, keyboard, keys):
        if self.state == "PAUSED":
            return

        self.background.update()

        if self.state == "VICTORY_MEME":
            self.update_victory_sequence()
            return

        if self.state != "PLAYING":
            return

        if self.hardcore_timer > 0:
            self.hardcore_timer -= 1
            if self.hardcore_timer == 0:
                self.finish_hardcore()

        self.player.update_cooldown()
        self.player.move(keyboard, keys)

        if self.player.score >= 1000 and self.boss is None:
            self.boss = Boss()
            self.enemies = []
            self.hardcore_can = None

        self.update_hardcore_can()
        self.update_background_music()

        if self.boss:
            self.boss.move()
            enemy_bullet = self.boss.update_shoot()
            if enemy_bullet:
                self.enemy_bullets.append(enemy_bullet)
        else:
            self.waves.update(self.enemies, self.player.score, False, self.hardcore_active)

        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.enemy_bullets.remove(bullet)

        for enemy in self.enemies[:]:
            speed_multiplier = 1.5 if self.hardcore_active else 1.0
            enemy.move(speed_multiplier)
            if enemy.is_off_screen():
                self.enemies.remove(enemy)

        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.finished:
                self.explosions.remove(explosion)

        CollisionManager.check_collisions(
            self.bullets,
            self.enemy_bullets,
            self.enemies,
            self.boss,
            self.player,
            self.explosions,
            self,
        )

        self.update_record()

        if self.state == "GAME_OVER":
            fadeout_music(0.7)

    def toggle_pause(self):
        if self.state == "PLAYING":
            self.state = "PAUSED"
            pause_all_audio()
        elif self.state == "PAUSED":
            self.state = "PLAYING"
            resume_all_audio()

    def go_home(self):
        """Vuelve a la portada desde la pantalla de pausa."""
        self.update_record()
        stop_gameplay_effects()
        stop_music()
        resume_all_audio()
        self.state = "MENU"

    def on_mouse_down(self, pos):
        if self.state == "PAUSED" and UIManager.get_home_button().collidepoint(pos):
            self.go_home()

    def on_key_down(self, key, keys):
        if self.state == "MENU":
            if key in [keys.RETURN, keys.SPACE]:
                self.state = "CHARACTER_SELECT"
        elif self.state == "CHARACTER_SELECT":
            if key == keys.LEFT:
                self.selected_character_index = (
                    self.selected_character_index - 1
                ) % len(self.CHARACTERS)
            elif key == keys.RIGHT:
                self.selected_character_index = (
                    self.selected_character_index + 1
                ) % len(self.CHARACTERS)
            elif key in [keys.RETURN, keys.SPACE]:
                self.start_game()
        elif self.state == "PLAYING":
            if key == keys.P:
                self.toggle_pause()
            elif key == keys.SPACE:
                new_bullet = self.player.shoot()
                if new_bullet:
                    self.bullets.append(new_bullet)
        elif self.state == "PAUSED":
            if key == keys.P:
                self.toggle_pause()
        elif self.state in ["GAME_OVER", "VICTORY"]:
            if key in [keys.R, keys.SPACE, keys.RETURN]:
                fadeout_effect("harry_maguire", 250)
                stop_music()
                self.state = "MENU"

    def draw_gameplay(self, screen):
        self.player.draw()
        if self.boss:
            self.boss.draw()
        if self.hardcore_can:
            self.hardcore_can.draw()
        for bullet in self.bullets:
            bullet.draw()
        for bullet in self.enemy_bullets:
            bullet.draw()
        for enemy in self.enemies:
            enemy.draw()
        for explosion in self.explosions:
            explosion.draw()
        UIManager.draw_hud(
            screen,
            self.player,
            self.boss,
            self.hardcore_timer,
            self.high_score,
        )

    def draw(self, screen):
        self.background.draw(screen)

        if self.state == "MENU":
            UIManager.draw_menu(screen, self.high_score)
        elif self.state == "CHARACTER_SELECT":
            UIManager.draw_character_select(screen, self.selected_character_index)
        elif self.state == "PLAYING":
            self.draw_gameplay(screen)
        elif self.state == "PAUSED":
            self.draw_gameplay(screen)
            UIManager.draw_paused(screen)
        elif self.state == "GAME_OVER":
            UIManager.draw_game_over(screen, self.player, self.high_score)
        elif self.state == "VICTORY":
            UIManager.draw_victory(screen, self.player, self.high_score)
        elif self.state == "VICTORY_MEME":
            self.victory_sequence.draw(screen)
