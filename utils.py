from abc import ABC, abstractmethod
from collections import namedtuple
from numbers import Number
import pygame as pg

class Scene(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def render(self, screen):
        pass


class Vector(namedtuple('Vector', ['x', 'y'])):
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __abs__(self):
        return (self.x**2 + self.y**2)**0.5

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

class BackButton():
    def __init__(self):
        self.font = pg.font.SysFont('Monospace', 30)
        self.image = pg.Surface([100, 50])
        self.rect = self.image.get_rect()
        self.rect.y = 50
        self.rect.x = 50

    def draw(self, screen):
        pg.draw.rect(screen, (255,255,255), self.rect, 3)
        text = self.font.render("Back", True, (255, 255, 255))
        screen.blit(text, (60,55))

def get_image(file):
    image = pg.image.load(file).convert_alpha()
    return image
