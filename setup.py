"""Settings for the Space Gem game."""
from utils import Vector


class Settings:
    FPS = 60


class PlatformerSettings(Settings):
    GRAVITY = Vector(0, 2)
