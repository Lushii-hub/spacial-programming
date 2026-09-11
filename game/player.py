import pygame
import math
from pgzero.actor import Actor
from pgzero.loaders import images
from config import WIDTH, HEIGHT
from game.audio import play
from game.bullet import Bullet

class Player:
    CHARACTER_CONFIG = {
        "nyan": {
            "image": "player/spaceship",
            "width": 114,
            "height": 70,
            "bullet": "bullets/laser_player",
            "bullet_size": (48, 32),
            "shoot_sound": "nyan_shoot",
            "music": "nyan_theme",
            "hardcore_music": "nyan_hardcore",
        },
        "kirby": {
            "image": "player/kirby",
            "width": 120,
            "height": 80,
            "bullet": "bullets/kirby_star",
            "bullet_size": (44, 44),
            "shoot_sound": "kirby_shoot",
            "music": "kirby_theme",
            "hardcore_music": "kirby_hardcore",
        },
    }

    def __init__(self, character="nyan"):
        # -------------------------------------------------------------
        # SEMANA 1: ATRIBUTOS DE LA NAVE
        # -------------------------------------------------------------
        # ACTIVIDAD 1: Define aca tus propios atributos usando 'self.'
        # Pista: Revisar WEEK1.md cuando termines de escribir los atributos notaras que tu nave aparecera en pantalla, pero aun no se podra mover
        # Es posible que te salgan errores en la terminal como "AttributeError: 'Player' object has no attribute 'width'" esto es una pista de lo que te falta, solo pon self. seguido del atributo que te falta :)

        self.character = character if character in self.CHARACTER_CONFIG else "nyan"
        character_config = self.CHARACTER_CONFIG[self.character]

        self.width = character_config["width"]
        self.height = character_config["height"]
        self.position_player_x = 100
        self.position_player_y = 300
        self.speed = 7
        self.base_speed = 7
        self.max_speed = 13
        self.score = 0
        self.lives = 5
        self.cooldown = 10
        self.cooldown_timer = 0
        self.rainbow_trail = []
        self.trail_timer = 0
        self.damage_timer = 0
        self.bullet_image = character_config["bullet"]
        self.bullet_width, self.bullet_height = character_config["bullet_size"]
        self.shoot_sound = character_config["shoot_sound"]
        self.music_name = character_config["music"]
        self.hardcore_music_name = character_config["hardcore_music"]

        # -------------------------------------------------------------
        # Descarga tu propia imagen de nave y guárdala en la carpeta 'images/player/'.
        # Luego, reemplaza "player/spaceship" por el nombre de tu archivo (sin .png o .jpg, o la extension que tenga).
        # -------------------------------------------------------------
        imagen_name = character_config["image"]

        surf = images.load(imagen_name)
        surf = pygame.transform.scale(surf, (self.width, self.height))
        
        self.actor = Actor(imagen_name, (self.position_player_x, self.position_player_y))
        self.actor._surf = surf
        self.actor._orig_surf = surf
        self.actor._update_pos()

    def move(self, keyboard, keys):
        # -------------------------------------------------------------
        # PROGRAMAR MOVIMIENTO
        # Recuerda la lógica del eje de coordenadas en la pantalla:
        # - Para subir: restamos en Y
        # - Para bajar: sumamos en Y
        # - Para la izquierda: restamos en X
        # - Para la derecha: sumamos en X
        # -------------------------------------------------------------

        # La nave acelera poco a poco conforme aumenta la puntuación.
        speed_bonus = min(6, self.score // 200)
        self.speed = min(self.max_speed, self.base_speed + speed_bonus)

        # Mover hacia arriba
        if keyboard[keys.UP]:
            self.actor.y -= self.speed

        # Completa el movimiento para las demás direcciones:
        # - Mover hacia abajo
        if keyboard[keys.DOWN]:
            self.actor.y += self.speed

        # - Mover hacia la izquierda
        if keyboard[keys.LEFT]:
            self.actor.x -= self.speed

        # - Mover hacia la derecha
        if keyboard[keys.RIGHT]:
            self.actor.x += self.speed


        # -------------------------------------------------------------
        # LÍMITES DE LA PANTALLA (Semana 1)
        # -------------------------------------------------------------
        half_width = self.width // 2
        half_height = self.height // 2

        if self.actor.x < half_width:
            self.actor.x = half_width
        if self.actor.x > WIDTH - half_width:
            self.actor.x = WIDTH - half_width
        if self.actor.y < half_height:
            self.actor.y = half_height
        if self.actor.y > HEIGHT - half_height:
            self.actor.y = HEIGHT - half_height

        self._update_rainbow_trail()

    def draw(self):
        self._draw_rainbow_aura()
        self.actor.draw()

    def _update_rainbow_trail(self):
        """Crea una estela que sigue la trayectoria vertical de la nave."""
        self.trail_timer += 1
        if self.trail_timer >= 2:
            self.trail_timer = 0
            self.rainbow_trail.append({
                "x": self.actor.left - 4,
                "y": self.actor.y,
                "life": 1.0,
                "phase": len(self.rainbow_trail) * 0.7,
            })

        for particle in self.rainbow_trail:
            particle["x"] -= 2.5 + self.speed * 0.15
            particle["life"] -= 0.055
            particle["phase"] += 0.22

        self.rainbow_trail = [p for p in self.rainbow_trail if p["life"] > 0]

    def _draw_rainbow_aura(self):
        display = pygame.display.get_surface()
        if display is None:
            return

        aura = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        colors = [
            (255, 55, 70),
            (255, 145, 35),
            (255, 235, 45),
            (55, 225, 85),
            (45, 155, 255),
            (145, 75, 245),
        ]

        for particle in self.rainbow_trail:
            life = particle["life"]
            alpha = max(0, min(175, int(175 * life)))
            length = max(10, int(46 * life))
            wave = math.sin(particle["phase"]) * 3
            start_y = particle["y"] - 18 + wave
            for index, color in enumerate(colors):
                rect = pygame.Rect(
                    int(particle["x"] - length),
                    int(start_y + index * 6),
                    length,
                    6,
                )
                pygame.draw.rect(aura, (*color, alpha), rect, border_radius=3)

        display.blit(aura, (0, 0))

    # -----------------------------------------------------------------
    # SEMANA 2: DISPAROS Y RECARGA
    # -----------------------------------------------------------------
    def update_cooldown(self):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= 1
        if self.damage_timer > 0:
            self.damage_timer -= 1

    def can_be_hit(self):
        return self.damage_timer <= 0

    def shoot(self):
        if self.cooldown_timer <= 0:
            self.cooldown_timer = self.cooldown
            bullet_x = self.actor.x + (self.width // 2)
            bullet_y = self.actor.y
            play(self.shoot_sound)
            return Bullet(
                bullet_x,
                bullet_y,
                image=self.bullet_image,
                width=self.bullet_width,
                height=self.bullet_height,
            )

        return None

    # -----------------------------------------------------------------
    # RECIBIR DAÑO Y DAÑO A ENEMIGOS
    # -----------------------------------------------------------------
    def take_damage(self):
        if not self.can_be_hit():
            return False

        self.damage_timer = 45
        self.lives -= 1
        defeated = self.lives <= 0
        if defeated:
            play("defeat")
        return defeated
