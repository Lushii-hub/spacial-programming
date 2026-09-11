import pygame
from pgzero.loaders import images

from config import WIDTH, HEIGHT


class VictorySequence:
    """Animación del meme que aparece al derrotar al jefe final."""

    FRAME_COUNT = 21
    FRAME_INTERVAL = 12  # 0,20 segundos por cuadro a 60 FPS
    FADE_DURATION = 90   # 1,5 segundos

    def __init__(self):
        self.frames = []
        self.timer = 0
        self.current_frame = 0
        self.announcement_started = False

        for index in range(self.FRAME_COUNT):
            frame_name = f"ui/victory_brain_{index:03d}"
            self.frames.append(images.load(frame_name))

        self.animation_duration = self.FRAME_COUNT * self.FRAME_INTERVAL
        self.total_duration = self.animation_duration + self.FADE_DURATION

    def update(self):
        self.timer += 1

        if self.timer < self.animation_duration:
            self.current_frame = min(
                len(self.frames) - 1,
                self.timer // self.FRAME_INTERVAL,
            )

    def should_announce_victory(self):
        if self.timer >= self.animation_duration and not self.announcement_started:
            self.announcement_started = True
            return True
        return False

    @property
    def finished(self):
        return self.timer >= self.total_duration

    def draw(self, screen):
        if not self.frames:
            return

        alpha = 255
        if self.timer > self.animation_duration:
            fade_progress = (
                (self.timer - self.animation_duration) / self.FADE_DURATION
            )
            alpha = max(0, int(255 * (1.0 - fade_progress)))

        frame = self.frames[self.current_frame].copy()
        frame.set_alpha(alpha)
        x = (WIDTH - frame.get_width()) // 2
        y = (HEIGHT - frame.get_height()) // 2

        try:
            screen.surface.blit(frame, (x, y))
        except Exception:
            pygame.display.get_surface().blit(frame, (x, y))
