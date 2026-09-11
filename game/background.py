import pygame
from pgzero.loaders import images

from config import WIDTH, HEIGHT

class BackgroundManager:
    def __init__(self, image_name="backgrounds/space", speed=1):
        self.image_name = image_name
        self.speed = speed
        self.bg_x = 0
        self._scroll_strip = None

    def _get_scroll_strip(self):
        """Prepara dos fondos espejados para que la unión sea continua."""
        if self._scroll_strip is None:
            try:
                raw_surf = images.load(self.image_name)

                # Escala sin deformar y recorta únicamente lo que queda fuera
                # de la pantalla. Así se conserva la proporción de la imagen.
                raw_width, raw_height = raw_surf.get_size()
                scale = max(WIDTH / raw_width, HEIGHT / raw_height)
                scaled_width = max(WIDTH, int(raw_width * scale))
                scaled_height = max(HEIGHT, int(raw_height * scale))
                scaled = pygame.transform.smoothscale(
                    raw_surf, (scaled_width, scaled_height)
                )
                crop_x = (scaled_width - WIDTH) // 2
                crop_y = (scaled_height - HEIGHT) // 2
                first_panel = scaled.subsurface(
                    pygame.Rect(crop_x, crop_y, WIDTH, HEIGHT)
                ).copy()

                # El segundo panel se refleja. Los bordes que se tocan son
                # idénticos y por eso nunca aparece el "final" del fondo.
                second_panel = pygame.transform.flip(first_panel, True, False)
                self._scroll_strip = pygame.Surface((WIDTH * 2, HEIGHT))
                self._scroll_strip.blit(first_panel, (0, 0))
                self._scroll_strip.blit(second_panel, (WIDTH, 0))
            except Exception:
                self._scroll_strip = None
        return self._scroll_strip

    def update(self):
        self.bg_x -= self.speed
        if self.bg_x <= -(WIDTH * 2):
            self.bg_x += WIDTH * 2

    def draw(self, screen):
        try:
            screen.fill((8, 10, 24))
        except Exception:
            try:
                screen.surface.fill((8, 10, 24))
            except Exception:
                pass

        strip = self._get_scroll_strip()
        if strip:
            try:
                screen.surface.blit(strip, (int(self.bg_x), 0))
                screen.surface.blit(strip, (int(self.bg_x) + WIDTH * 2, 0))
            except Exception:
                try:
                    screen.blit(strip, (int(self.bg_x), 0))
                    screen.blit(strip, (int(self.bg_x) + WIDTH * 2, 0))
                except Exception:
                    pass
        else:
            try:
                screen.blit(self.image_name, (int(self.bg_x), 0))
                screen.blit(self.image_name, (int(self.bg_x) + WIDTH, 0))
            except Exception:
                pass
