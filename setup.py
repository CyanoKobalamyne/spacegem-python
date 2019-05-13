"""Settings for the Space Gem game."""
from pygame import Color

from utils import Vector


class GameSettings:
    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


class PlatformerSettings:
    BG_COLOR = Color('white')
    PPU = 100
    BLOB_SIZE = 1
    PLATFORM_HEIGHT = 1
    GRAVITY = Vector(0, 0.02)
    RUN_SPEED = 1
    JUMP_SPEED = 1
    SOUND_RADIUS = 2
    FONT_FACE = 'Arial'
    FONT_SIZE = 24
    TEXT_COLOR = Color('black')
    TEXT_MARGIN = Vector(10, 5)
    TEXT_BG_COLOR = Color('lightblue')
