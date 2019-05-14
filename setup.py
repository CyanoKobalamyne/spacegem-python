"""Settings for the Space Gem game."""
from pygame import Color

from utils import Vector


class GameSettings:
    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


class PlatformerSettings(GameSettings):
    BG_COLOR = Color('white')
    BLOB_SIZE = 100
    PLATFORM_HEIGHT = 100
    GRAVITY = Vector(0, 2)
    RUN_SPEED = 50
    JUMP_SPEED = 100
    SOUND_RADIUS = 150
    FONT_FACE = 'Arial'
    FONT_SIZE = 24
    TEXT_COLOR = Color('black')
    TEXT_MARGIN = Vector(10, 5)
    TEXT_BG_COLOR = Color('lightblue')
