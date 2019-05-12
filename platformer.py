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


FPS = 60
GRAVITY = Vector(0, -2)


class NotePlatformerScene:
    def __init__(self):
        self.platforms = Group()
        self.gems = Group()
        self.blobs = Group()

        platforms = [
            Platform(position=Vector(0, 700)),
            Platform(position=Vector(700, 700)),
        ]
        gems = [
            Gem(position=Vector(1000, 600)),
        ]
        self.player = Player(position=Vector(200, 600))

        for blob in platforms:
            self.blobs.add(blob)
            self.platforms.add(blob)
        for blob in gems:
            self.blobs.add(blob)
            self.gems.add(blob)
        self.blobs.add(self.player)

    def render(self, screen):
        screen.fill(Color('white'))
        self.blobs.draw(screen)

    def update(self):
        self.blobs.update()

        # Handle player-platform collisions.
        for platform in pygame.sprite.spritecollide(
                self.player, self.platforms, False):
            self.player.collide(platform)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()

            if event.type == pygame.KEYUP:
                if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                    self.player.stop_horizontal()
                if event.key in {pygame.K_UP}:
                    self.player.stop_vertical()


class Blob(Sprite):
    def __init__(self, width, height, color, position, velocity=Vector(0, 0)):
        super().__init__()
        self.width = width
        self.height = height
        self.position = position
        self.velocity = velocity

        self.image = Surface((width, height))
        self.image.fill(Color(color))
        self.rect = self.image.get_rect()

    def _normalize(self):
        pos_diff = self.position - Vector(self.rect.x, self.rect.y)
        self.rect.move_ip(*pos_diff)

    def update(self):
        self.position += self.velocity / FPS
        self._normalize()

    def collide(self, other):
        if self.velocity.x > 0:
            dx = other.position.x - (self.position.x + self.width)
        elif self.velocity.x < 0:
            dx = (other.position.x + other.width) - self.position.x
        else:
            dx = 0

        if self.velocity.y > 0:
            dy = other.position.y - (self.position.y + self.height)
        elif self.velocity.y < 0:
            dy = self.position.y - (other.position.y + other.height)
        else:
            dy = 0

        print(dx, dy)
        if dy == 0 or abs(dx) <= abs(dy):
            self.velocity = Vector(0, self.velocity.y)
            self.position += Vector(dx, 0)
        if dx == 0 or abs(dy) <= abs(dx):
            self.velocity = Vector(self.velocity.x, 0)
            self.position += Vector(0, dy)

        self._normalize()


class FallingBlob(Blob):
    def update(self):
        self.velocity -= GRAVITY
        super().update()


class Platform(Blob):
    def __init__(self, **kwargs):
        super().__init__(width=500, height=100, color='blue', **kwargs)


class Player(FallingBlob):
    def __init__(self, **kwargs):
        super().__init__(width=100, height=100, color='green', **kwargs)
        self.v_run = 50
        self.v_jump = -200

    def go_left(self):
        self.velocity = Vector(-self.v_run, self.velocity.y)

    def go_right(self):
        self.velocity = Vector(self.v_run, self.velocity.y)

    def jump(self):
        self.velocity = Vector(self.velocity.x, self.v_jump)

    def stop_horizontal(self):
        self.velocity = Vector(0, self.velocity.y)

    def stop_vertical(self):
        self.velocity = Vector(self.velocity.x, 0)


class Gem(Blob):
    def __init__(self, **kwargs):
        super().__init__(width=100, height=100, color='red', **kwargs)


def main():
    pygame.init()

    size = [1200, 800]
    screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
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
