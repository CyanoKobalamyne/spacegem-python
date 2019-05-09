"""Platformer scene for Level 1."""
from collections import namedtuple
from numbers import Number

import pygame
import pygame.display
import pygame.event
import pygame.sprite
import pygame.time
from pygame import Color, Surface
from pygame.sprite import Group, Sprite


FPS = 60


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


class NotePlatformerScene:
    def __init__(self):
        self.platforms = Group()
        self.enemies = Group()
        self.blobs = Group()

        platforms = [
            Platform(position=Vector(0, 50)),
            Platform(position=Vector(110, 50)),
            Platform(position=Vector(220, 50)),
        ]
        enemies = [
            Enemy(position=Vector(100, 40)),
        ]
        self.player = Player(position=Vector(40, 40))

        for blob in platforms:
            self.blobs.add(blob)
            self.platforms.add(blob)
        for blob in enemies:
            self.blobs.add(blob)
            self.enemies.add(blob)
        self.blobs.add(self.player)

    def render(self, screen):
        screen.fill(Color('white'))
        self.blobs.draw(screen)

    def update(self):
        self.blobs.update()

    def handle_events(self, events):
        for event in events:
            print(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()
 
            if event.type == pygame.KEYUP:
                if event.key in {pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP}:
                    self.player.stop()


class Blob(Sprite):
    def __init__(self, width, height, color, position, velocity=Vector(0, 0)):
        super().__init__()
        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = self.image.get_rect()
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position += self.velocity / FPS
        pos_diff = self.position - Vector(self.rect.x, self.rect.y)
        self.rect.move_ip(*pos_diff)


class Platform(Blob):
    def __init__(self, **kwargs):
        super().__init__(100, 20, 'blue', **kwargs)


class Player(Blob):
    def __init__(self, **kwargs):
        super().__init__(10, 10, 'green', **kwargs)
        self.v_run = Vector(20, 0)
        self.v_jump = Vector(0, -5)

    def go_left(self):
        self.velocity = -self.v_run

    def go_right(self):
        self.velocity = self.v_run

    def jump(self):
        self.velocity = self.v_jump

    def stop(self):
        self.velocity = Vector(0, 0)


class Enemy(Blob):
    def __init__(self, **kwargs):
        super().__init__(10, 10, 'red', velocity=Vector(-10, 0), **kwargs)


def main():
    pygame.init()

    size = [600, 400]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Test platformer')

    level = NotePlatformerScene()
    clock = pygame.time.Clock()

    while True:
        events = pygame.event.get()
        if any(event.type == pygame.QUIT for event in events):
            break

        level.handle_events(events)
        level.update()
        level.render(screen)
        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
