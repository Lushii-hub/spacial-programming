# type: ignore
import pgzrun
from game.game_manager import GameManager
from config import WIDTH, HEIGHT, TITLE

game_manager = GameManager()

def draw():
    game_manager.draw(screen)

def update():
    game_manager.update(keyboard, keys)

def on_key_down(key):
    game_manager.on_key_down(key, keys)

def on_mouse_down(pos):
    game_manager.on_mouse_down(pos)

pgzrun.go()
