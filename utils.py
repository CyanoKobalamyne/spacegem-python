from abc import ABC, abstractmethod
from collections import namedtuple
from numbers import Number

import pygame.draw
import pygame.font
from pygame import Rect, Surface
from pygame.sprite import Group


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
        self.font = pygame.font.SysFont('Monospace', 30)
        self.image = Surface([100, 50])
        self.rect = self.image.get_rect()
        self.rect.y = 50
        self.rect.x = 50

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        text = self.font.render("Back", True, (255, 255, 255))
        screen.blit(text, (60, 55))


class HorizontalScrollingGroup(Group):
    def __init__(self, target, screen_size, world_size, margin, *sprites):
        super().__init__(*sprites)
        self.target = target
        self.margin = margin
        self.world_size = world_size
        self.camera = Rect(0, 0, *screen_size)

        self.add(target)

    def update(self, *args):
        super().update(*args)
        if self.target.rect.left < self.camera.left + self.margin:
            self.camera.left = max(0, self.target.rect.left - self.margin)
        elif self.camera.right - self.margin < self.target.rect.right:
            self.camera.right = min(self.target.rect.right + self.margin,
                                    self.world_size[0])

    def draw(self, surface):
        sprites = self.sprites()
        for spr in sprites:
            new_rect = spr.rect.move(-Vector(*self.camera.topleft))
            self.spritedict[spr] = surface.blit(spr.image, new_rect)
        self.lostsprites = []


def get_image(file):
    image = pygame.image.load(file).convert_alpha()
    return image
