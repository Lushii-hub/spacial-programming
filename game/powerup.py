"""Lata especial del modo HARDCORE."""

import pygame
from pgzero.actor import Actor
from pgzero.loaders import images


class HardcoreCan:
    def __init__(self, x, y):
        self.width = 52
        self.height = 76
        self.speed = 3
        self.actor = Actor("powerups/hardcore", (x, y))

        surf = images.load("powerups/hardcore")
        surf = pygame.transform.scale(surf, (self.width, self.height))
        self.actor._surf = surf
        self.actor._orig_surf = surf
        self.actor._update_pos()

    def move(self):
        self.actor.x -= self.speed

    def is_off_screen(self):
        return self.actor.right < 0

    def draw(self):
        self.actor.draw()
