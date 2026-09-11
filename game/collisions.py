from game.explosion import Explosion
from game.audio import play

class CollisionManager:
    @staticmethod
    def check_collisions(bullets, enemy_bullets, enemies, boss, player, explosions, game):
        for b in bullets[:]:
            for e in enemies[:]:
                if b.actor.colliderect(e.actor):
                    bullets.remove(b)
                    enemies.remove(e)
                    player.score += e.points
                    play("impact")
                    explosions.append(Explosion(e.actor.x, e.actor.y))
                    break

            if boss and b.actor.colliderect(boss.actor):
                if b in bullets: bullets.remove(b)
                play("impact")
                explosions.append(Explosion(b.actor.x, b.actor.y))
                if boss.take_damage(1):
                    game.start_victory_sequence()
                    return

        for eb in enemy_bullets[:]:
            if eb.actor.colliderect(player.actor):
                enemy_bullets.remove(eb)
                CollisionManager._damage_player(player, explosions, game)

        for e in enemies[:]:
            if e.actor.colliderect(player.actor):
                enemies.remove(e)
                CollisionManager._damage_player(player, explosions, game)

        if boss and boss.actor.colliderect(player.actor):
            CollisionManager._damage_player(player, explosions, game)

    @staticmethod
    def _damage_player(player, explosions, game):
        if not player.can_be_hit():
            return

        play("impact")
        explosions.append(Explosion(player.actor.x, player.actor.y))
        if player.take_damage():
            game.state = "GAME_OVER"
