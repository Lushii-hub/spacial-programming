import pygame
from pgzero.actor import Actor
from pgzero.loaders import images
from config import WIDTH

class Bullet:
    def __init__(self, x, y, speed=12, image="bullets/laser_player", width=48, height=32):
        self.speed = speed
        self.width = width
        self.height = height
        self.actor = Actor(image, (x, y))

        try:
            surf = images.load(image)
            surf = pygame.transform.scale(surf, (self.width, self.height))
            self.actor._surf = surf
            self.actor._orig_surf = surf
            self.actor._update_pos()
        except Exception:
            pass

    def move(self):
        self.actor.x += self.speed

    def is_off_screen(self):
        return self.actor.x > WIDTH + self.width

    def draw(self):
        self.actor.draw()

class EnemyBullet(Bullet):
    def __init__(self, x, y, speed=8, image="bullets/laser_enemy"):
        super().__init__(x, y, speed, image)

    def move(self):
        self.actor.x -= self.speed

    def is_off_screen(self):
        return self.actor.x < -20
