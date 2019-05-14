"""Settings for the Space Gem game."""
import pygame
from pygame import Color

from utils import Vector


class GameSettings:
    FPS = 60
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600


class PlatformerSettings:
    BG_COLOR = Color('black')
    PPU = 100
    BLOB_SIZE = 1
    PLATFORM_HEIGHT = 1
    GRAVITY = Vector(0, 5)
    RUN_SPEED = 1
    JUMP_SPEED = 3
    SOUND_RADIUS = 2
    SCROLL_MARGIN = 1
    JUMP_TIME = 0.5
    LEFT_KEYS = {pygame.K_LEFT, pygame.K_a}
    RIGHT_KEYS = {pygame.K_RIGHT, pygame.K_d}
    JUMP_KEYS = {pygame.K_UP, pygame.K_w, pygame.K_SPACE}
    TEXT_BGCOLOR = Color('black')
    TEXT_STYLE = {
        "text": {
            "margin": Vector(10, 5),
        },
        "paragraph": {
            "spacing": 10,
        },
        "font": {
            "family": 'Monospace',
            "size": 24,
            "color": Color('white'),
        }
    }
    OVERLAY_COLOR = Color(255, 255, 255, 127)
