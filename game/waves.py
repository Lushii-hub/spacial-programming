import random
from game.enemy import Enemy
from config import WIDTH, HEIGHT

class WaveManager:
    def __init__(self):
        self.spawn_timer = 0

    def update(self, enemies, player_score, boss_spawned, hardcore=False):
        if player_score >= 1000 or boss_spawned:
            return

        self.spawn_timer += 1
        spawn_interval = 28 if hardcore else 45
        if self.spawn_timer % spawn_interval == 0:
            y_pos = random.randint(50, max(60, HEIGHT - 50))
            enemies.append(Enemy(WIDTH + 40, y_pos, "Enemy"))
