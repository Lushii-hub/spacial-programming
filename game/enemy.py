import pygame
from pgzero.actor import Actor
from pgzero.loaders import images

class Enemy:
    def __init__(self, x, y, enemy_type="Enemy", image_name="enemies/alien", width=56, height=48):
        self.type_name = enemy_type
        self.image_name = image_name
        self.width = width
        self.height = height
        self.actor = Actor(image_name, (x, y))

        try:
            surf = images.load(image_name)
            surf = pygame.transform.scale(surf, (width, height))
            self.actor._surf = surf
            self.actor._orig_surf = surf
            self.actor._update_pos()
        except Exception:
            pass

        self.speed = 4
        self.health = 1
        self.points = 100

    def move(self, speed_multiplier=1.0):
        self.actor.x -= self.speed * speed_multiplier

    def take_damage(self, amount=1):
        self.health -= amount
        return self.health <= 0

    def is_off_screen(self):
        return self.actor.x < -40

    def draw(self):
        self.actor.draw()
