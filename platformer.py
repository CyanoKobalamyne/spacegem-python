"""Platformer scene for Level 1."""
from collections import namedtuple
from numbers import Number

import pygame
import pygame.display
import pygame.sprite
import pygame.time
from pygame import Color, Surface
from pygame.sprite import Group, GroupSingle, Sprite


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
        self.__add__(-other)

    def __mul__(self, other):
        if isinstance(other, Number):
            return Vector(other * self.x, other * self.y)
        else:
            raise TypeError(f"can't multiply vector by {type(other)}")

    def __rmul__(self, other):
        return self.__mul__(other)


class NotePlatformerScene:
    def __init__(self):
        self.player = GroupSingle()
        self.platforms = Group()
        self.enemies = Group()
        self.objects = [self.platforms, self.enemies, self.player]

        self.load()

    def load(self):
        self.player.add(Player(position=Vector(40, 40)))
        self.platforms.add(Platform(position=Vector(0, 50)))
        self.platforms.add(Platform(position=Vector(110, 50)))
        self.platforms.add(Platform(position=Vector(220, 50)))
        self.enemies.add(Enemy(position=Vector(100, 40)))

    def render(self, screen):
        screen.fill(Color('white'))
        for sprite_group in self.objects:
            sprite_group.draw(screen)

    def update(self):
        for sprite_group in self.objects:
            sprite_group.update()

    def handle_events(self, events):
        pass


class Blob(Sprite):
    def __init__(self, width, height, color, position, velocity=Vector(0, 0)):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
        self.velocity = velocity

    def update(self):
        self.rect.move_ip(*self.velocity)


class Platform(Blob):
    def __init__(self, **kwargs):
        super().__init__(100, 20, 'blue', **kwargs)


class Player(Blob):
    def __init__(self, **kwargs):
        super().__init__(10, 10, 'green', velocity=Vector(20, 0), **kwargs)


class Enemy(Blob):
    def __init__(self, **kwargs):
        super().__init__(10, 10, 'red', velocity=Vector(-10, 0), **kwargs)


def main():
    pygame.init()

    size = [600, 400]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
    pygame.display.set_caption('Test platformer')

    level = NotePlatformerScene()
    clock = pygame.time.Clock()
    fps = 2

    while True:
        if any(event.type == pygame.QUIT for event in pygame.event.get()):
            break

        level.update()
        level.render(screen)
        clock.tick(fps)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
