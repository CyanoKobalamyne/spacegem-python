"""Settings for the Space Gem game."""
from utils import Vector


class GameSettings:
    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


class PlatformerSettings(GameSettings):
    BLOB_SIZE = 100
    GRAVITY = Vector(0, 2)
    RUN_SPEED = 50
    JUMP_SPEED = 100
    SOUND_RADIUS = 150
