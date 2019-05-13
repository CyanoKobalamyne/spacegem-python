"""Settings for the Space Gem game."""
import pygame
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
    GRAVITY = Vector(0, 0.1)
    RUN_SPEED = 1
    JUMP_SPEED = 3
    SOUND_RADIUS = 2
    FONT_FACE = 'Arial'
    FONT_SIZE = 24
    TEXT_COLOR = Color('black')
    TEXT_MARGIN = Vector(10, 5)
    TEXT_BG_COLOR = Color('lightblue')
    SCROLL_MARGIN = 1
    JUMP_TIME = 0.5
    LEFT_KEYS = {pygame.K_LEFT, pygame.K_a}
    RIGHT_KEYS = {pygame.K_RIGHT, pygame.K_d}
    JUMP_KEYS = {pygame.K_UP, pygame.K_w, pygame.K_SPACE}
