"""Platformer scene for Level 1."""
from collections import namedtuple
import pygame as pg


Vector = namedtuple('Vector', ['x', 'y'])


class NotePlatformerScene:
    def __init__(self):
        self.player = Player()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.objects = [self.platforms, self.enemies, self.player]

    def render(self, screen):
        screen.fill(pg.Color('white'))
        for sprite_group in self.objects:
            sprite_group.draw(screen)

    def update(self):
        for sprite_group in self.objects:
            sprite_group.update()

    def handle_events(self, events):
        pass


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()


class Platform(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()


class Enemy(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
