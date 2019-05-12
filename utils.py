from collections import namedtuple
from numbers import Number

import pygame as pg

RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 204, 0)
TEAL = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 255)
GEM_COLORS = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, RED]

class Gem(pg.sprite.Sprite): 
    def __init__(self, x, y, tone):
        super().__init__()

        self.image = pg.Surface([40, 40])
        self.image.fill(GEM_COLORS[tone])
     
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.tone = tone

class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError

class SceneManager(object):
    def __init__(self, firstScene):
        self.go_to(firstScene)

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self


class Vector(namedtuple('Vector', ['x', 'y'])):
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __add__(self, other):
        if not isinstance(other, Vector):
            raise TypeError(f"{other} is not a vector")

        x = self.x + other.x
        y = self.y + other.y
        return Vector(x, y)

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(other * self.x, other * self.y)
        else:
            raise TypeError(f"can't multiply vector by {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self.__mul__(1 / other)
