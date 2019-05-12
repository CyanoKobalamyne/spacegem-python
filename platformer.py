"""Platformer scene for Level 1."""
import pygame
import pygame.display
import pygame.event
import pygame.font
import pygame.mixer
import pygame.mouse
import pygame.sprite
import pygame.time
from pygame import Color, Surface
from pygame.sprite import Group, Sprite

import menus
from setup import PlatformerSettings as Settings
from utils import Scene, Vector


class NotePlatformerScene(Scene):
    def __init__(self, state):
        self.state = state
        self.platforms = Group()
        self.gems = Group()
        self.blobs = Group()

        platforms = [
            Platform(position=Vector(
                    0, Settings.SCREEN_HEIGHT - Settings.BLOB_SIZE)),
            Platform(position=Vector(
                    Settings.SCREEN_WIDTH / 2 + Settings.BLOB_SIZE * 1.5,
                    Settings.SCREEN_HEIGHT - Settings.BLOB_SIZE)),
        ]
        gems = [
            Gem(position=Vector(
                    0, Settings.SCREEN_HEIGHT - 2 * Settings.BLOB_SIZE),
                note=2),
            Gem(position=Vector(
                    Settings.SCREEN_WIDTH - 2 * Settings.BLOB_SIZE,
                    Settings.SCREEN_HEIGHT - 2 * Settings.BLOB_SIZE),
                note=0,
                winner=True),
        ]
        self.player = Player(position=Vector(
            3 * Settings.BLOB_SIZE,
            Settings.SCREEN_HEIGHT - 2 * Settings.BLOB_SIZE))

        for blob in platforms:
            self.blobs.add(blob)
            self.platforms.add(blob)
        for blob in gems:
            self.blobs.add(blob)
            self.gems.add(blob)
        self.blobs.add(self.player)

        self.channels = {}

        self.welcome = WelcomeText()
        self.at_welcome = True

    def update(self):
        if self.at_welcome:
            return

        self.blobs.update()

        # Handle player-platform collisions.
        for platform in pygame.sprite.spritecollide(
                self.player, self.platforms, False):
            self.player.collide(platform)

        # Handle collisions with gems.
        for gem in pygame.sprite.spritecollide(
                self.player, self.gems, False):
            if gem.winner:
                self.manager.go_to(menus.WinScene(self.state))
            else:
                self.manager.go_to(menus.LoseScene(self.state))

        # Play sound near gems.
        for gem in self.gems:
            distance = (abs(self.player.center - gem.center)
                        - Settings.BLOB_SIZE)
            if distance <= Settings.SOUND_RADIUS:
                vol_ratio = 1 - distance / Settings.SOUND_RADIUS
                self._play_gem_sound(gem, vol_ratio)
            else:
                self._stop_gem_sound(gem)

    def handle_events(self, events):
        for event in events:
            if self.at_welcome:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.welcome.rect.collidepoint(pos):
                        self._play_goal_sound()
                    else:
                        self.at_welcome = False
                continue

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    # Check if there are platforms underneath.
                    self.player.position += Vector(0, 2)
                    self.player._normalize()
                    can_jump = len(pygame.sprite.spritecollide(
                        self.player, self.platforms, False)) > 0
                    self.player.position -= Vector(0, 2)
                    self.player._normalize()
                    if can_jump:
                        self.player.jump()

            if event.type == pygame.KEYUP:
                if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                    self.player.stop()

    def render(self, screen):
        screen.fill(Settings.BG_COLOR)
        self.blobs.draw(screen)
        if self.at_welcome:
            self.welcome.draw(screen)

    def _play_goal_sound(self):
        winning_gems = (gem for gem in self.gems if gem.winner)
        try:
            gem = next(winning_gems)
        except StopIteration:
            raise RuntimeError("no winning gem")
        self._play_gem_sound(gem, 1, loop=False)

    def _play_gem_sound(self, gem, volume, loop=True):
        if gem not in self.channels or self.channels[gem].get_sound() is None:
            channel = pygame.mixer.find_channel()
            if channel is None:
                raise RuntimeError("no free audio channel found")
            self.channels[gem] = channel
            channel.play(gem.sound, loops=-1 if loop else 0)
        self.channels[gem].set_volume(volume)

    def _stop_gem_sound(self, gem):
        if gem in self.channels:
            self.channels[gem].stop()
            del self.channels[gem]


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

        self._normalize()

    def _normalize(self):
        pos_diff = self.position - Vector(self.rect.x, self.rect.y)
        self.rect.move_ip(*pos_diff)
        diagonal = Vector(self.width, self.height)
        self.center = self.position + diagonal / 2

    def update(self):
        self.position += self.velocity / Settings.FPS
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

        if dy == 0 or abs(dx) <= abs(dy):
            self.velocity = Vector(0, self.velocity.y)
            self.position += Vector(dx, 0)
        if dx == 0 or abs(dy) <= abs(dx):
            self.velocity = Vector(self.velocity.x, 0)
            self.position += Vector(0, dy)

        self._normalize()


class FallingBlob(Blob):
    def update(self):
        self.velocity += Settings.GRAVITY
        super().update()


class Platform(Blob):
    def __init__(self, **kwargs):
        super().__init__(width=Settings.SCREEN_WIDTH / 2,
                         height=Settings.BLOB_SIZE,
                         color='blue', **kwargs)


class Player(FallingBlob):
    def __init__(self, **kwargs):
        super().__init__(width=Settings.BLOB_SIZE, height=Settings.BLOB_SIZE,
                         color='black', **kwargs)

    def go_left(self):
        self.velocity = Vector(-Settings.RUN_SPEED, self.velocity.y)

    def go_right(self):
        self.velocity = Vector(Settings.RUN_SPEED, self.velocity.y)

    def jump(self):
        self.velocity = Vector(self.velocity.x, -Settings.JUMP_SPEED)

    def stop(self):
        self.velocity = Vector(0, self.velocity.y)


class Gem(Blob):
    def __init__(self, note, winner=False, **kwargs):
        color = 'green' if winner else 'red'
        super().__init__(width=Settings.BLOB_SIZE, height=Settings.BLOB_SIZE,
                         color=color, **kwargs)
        self.note = note
        self.winner = winner

        # Get sound for this note.
        sound_path = f"./sounds/{note}.wav"
        self.sound = pygame.mixer.Sound(sound_path)


class WelcomeText:
    def __init__(self):
        font = pygame.font.SysFont(Settings.FONT_FACE, Settings.FONT_SIZE)
        text = "Objective: find the gem with this sound (click to play)"
        text_image = font.render(text, True, Settings.TEXT_COLOR)
        margin = Settings.TEXT_MARGIN
        size = Vector(*text_image.get_size())
        size += 2 * margin
        self.image = Surface(size)
        self.image.fill(Settings.TEXT_BG_COLOR)
        self.image.blit(text_image, margin)
        self.rect = self.image.get_rect()

    def draw(self, screen):
        offset = Vector(*screen.get_size()) / 2
        offset -= Vector(*self.image.get_size()) / 2
        screen.blit(self.image, offset)
        self.rect = self.image.get_rect()
        self.rect.move_ip(*offset)


def main():
    pygame.init()

    size = (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT)
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
        clock.tick(Settings.FPS)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
