import pygame
from pgzero.actor import Actor
from pgzero.loaders import images
from game.bullet import EnemyBullet
from game.audio import play
from config import WIDTH, HEIGHT

class Boss:
    def __init__(self, x=None, y=None, image_name="enemies/boss", width=170, height=170):
        if x is None: x = WIDTH - 100
        if y is None: y = HEIGHT // 2
        self.image_name = image_name
        self.actor = Actor(image_name, (x, y))
        self.frames = []
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_interval = 2

        try:
            frame_names = [image_name]
            frame_names.extend(f"enemies/boss_{index:03d}" for index in range(1, 60))

            for frame_name in frame_names:
                surf = images.load(frame_name)
                surf = pygame.transform.scale(surf, (width, height))
                self.frames.append(surf)

            self.width = width
            self.height = height
            self._show_current_frame()
        except Exception:
            self.width = width or 160
            self.height = height or 140

        self.speed_y = 3
        self.direction_y = 1
        self.health = 15
        self.max_health = 15
        self.shoot_timer = 0

    def move(self):
        self._update_animation()
        self.actor.y += self.speed_y * self.direction_y
        if self.actor.y < 80:
            self.actor.y = 80
            self.direction_y = 1
        elif self.actor.y > HEIGHT - 80:
            self.actor.y = HEIGHT - 80
            self.direction_y = -1

    def _update_animation(self):
        if len(self.frames) <= 1:
            return

        self.animation_timer += 1
        if self.animation_timer >= self.animation_interval:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self._show_current_frame()

    def _show_current_frame(self):
        if not self.frames:
            return

        center = self.actor.pos
        surf = self.frames[self.current_frame]
        self.actor._surf = surf
        self.actor._orig_surf = surf
        self.actor._update_pos()
        self.actor.pos = center

    def update_shoot(self):
        self.shoot_timer += 1
        # El intervalo permite escuchar completo el sonido especial del jefe.
        if self.shoot_timer >= 120:
            self.shoot_timer = 0
            bullet_x = self.actor.x - (self.width // 2)
            play("boss_shoot")
            return EnemyBullet(bullet_x, self.actor.y)
        return None

    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0

    def draw(self):
        self.actor.draw()
