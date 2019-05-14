"""Platformer scene for Level 1."""
import os

import pygame.display
import pygame.event
import pygame.font
import pygame.image
import pygame.mixer
import pygame.mouse
import pygame.sprite
import pygame.time
from pygame import Color, Surface
from pygame.sprite import Group, Sprite

import menus
from setup import GameSettings as GS
from setup import PlatformerSettings as PS
from utils import Button, HorizontalScrollingGroup, Scene, TextBox, Vector
from worlds import World_1


class NotePlatformerScene(Scene):
    def __init__(self, state):
        level = getattr(World_1, f"Level_{state['level'] + 1}")

        self.state = state
        self.player = Player(position=Vector(*level.player))

        self.platforms = Group()
        self.gems = Group()
        level_width = PS.PPU * max(map(lambda p: p[0] + p[2], level.platforms))
        self.blobs = HorizontalScrollingGroup(
            self.player, (GS.SCREEN_WIDTH, GS.SCREEN_HEIGHT),
            (level_width, GS.SCREEN_HEIGHT), PS.SCROLL_MARGIN * PS.PPU)

        for x, y, width, height in level.platforms:
            platform = Platform(width=width, height=height,
                                position=Vector(x, y))
            self.blobs.add(platform)
            self.platforms.add(platform)
        for x, y, note, winner in level.gems:
            gem = Gem(note, winner=winner, position=Vector(x, y))
            self.blobs.add(gem)
            self.gems.add(gem)
            if winner:
                goal_path = os.path.join("sounds", "short", f"{note}.wav")
                self.goal_sound = pygame.mixer.Sound(goal_path)

        self.channels = {}

        self.greeting = TextBox(
            "Your task is to find the gem which emits a certain sound.\nYou "
            "can listen to the sound by clicking on this box. You can also "
            "listen to it during the game by clicking on the \"Goal\" button "
            "in the corner.\nClick outside the box to start.",
            bgcolor=PS.TEXT_BGCOLOR,
            max_size=(GS.SCREEN_WIDTH * 0.6, GS.SCREEN_HEIGHT * 0.6),
            style=PS.TEXT_STYLE)
        self.started = False

        self.sound_btn = Button("Target sound", Vector(50, 50), Vector(10, 5))

    def update(self):
        if not self.started:
            return

        self.blobs.update()

        # Handle player-platform collisions.
        for platform in pygame.sprite.spritecollide(
                self.player, self.platforms, False):
            self.player.collide(platform)

        # Play sound near gems.
        for gem in self.gems:
            distance = (abs(Vector(*self.player.rect.center)
                            - Vector(*gem.rect.center))
                        - PS.BLOB_SIZE)
            if distance <= PS.SOUND_RADIUS:
                vol_ratio = 1 - distance / PS.SOUND_RADIUS
                self._play_gem_sound(gem, vol_ratio)
            else:
                self._stop_gem_sound(gem)

        # Handle collisions with gems.
        for gem in pygame.sprite.spritecollide(
                self.player, self.gems, False):
            # End condition.
            if gem.winner:
                self.manager.go_to(menus.WinScene(self.state))
            else:
                self.manager.go_to(menus.LoseScene(self.state))
            # Turn off sound.
            self._stop_all_sounds()

    def handle_events(self, events):
        for event in events:
            # Handle interaction with greeting box.
            if not self.started:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if self.greeting.rect.collidepoint(pos):
                        self.goal_sound.play()
                    else:
                        self.started = True
                continue

            # Handle navigation key presses.
            if event.type == pygame.KEYDOWN:
                if event.key in PS.LEFT_KEYS:
                    self.player.go_left()
                elif event.key in PS.RIGHT_KEYS:
                    self.player.go_right()
                elif event.key in PS.JUMP_KEYS:
                    if self.player.can_jump(self.platforms):
                        self.player.jump()
            elif event.type == pygame.KEYUP:
                if event.key in PS.LEFT_KEYS:
                    self.player.stop_left()
                elif event.key in PS.RIGHT_KEYS:
                    self.player.stop_right()
                elif event.key in PS.JUMP_KEYS:
                    self.player.stop_jump()
            # Handle clicking sound button.
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.sound_btn.rect.collidepoint(pygame.mouse.get_pos()):
                    self.goal_sound.play()

    def render(self, screen):
        screen.fill(PS.BG_COLOR)
        self.blobs.draw(screen)
        self.sound_btn.draw(screen)
        if not self.started:
            overlay = Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill(PS.OVERLAY_COLOR)
            screen.blit(overlay, (0, 0))
            self.greeting.draw(screen)

    def _play_gem_sound(self, gem, volume, loop=True):
        gem.sound.set_volume(volume)
        gem.sound.play(loops=-1 if loop else 0)

    def _stop_gem_sound(self, gem):
        gem.sound.stop()

    def _stop_all_sounds(self):
        for gem in self.gems:
            gem.sound.stop()


class Blob(Sprite):
    def __init__(self, position, velocity=Vector(0, 0)):
        super().__init__()
        self.position = position
        self.velocity = velocity
        self.rect = self.image.get_rect()
        self._normalize()

    def _normalize(self):
        rect_position = Vector(self.rect.x, self.rect.y) / PS.PPU
        pos_diff = self.position - rect_position
        self.rect.move_ip(*(pos_diff * PS.PPU))

    def update(self):
        self.position += self.velocity / GS.FPS
        self._normalize()

    def width(self):
        return self.rect.width / PS.PPU

    def height(self):
        return self.rect.height / PS.PPU

    def collide(self, other):
        if self.velocity.x > 0:
            dx = other.position.x - (self.position.x + self.width())
        elif self.velocity.x < 0:
            dx = (other.position.x + other.width()) - self.position.x
        else:
            dx = 0

        if self.velocity.y > 0:
            dy = other.position.y - (self.position.y + self.height())
        elif self.velocity.y < 0:
            dy = self.position.y - (other.position.y + other.height())
        else:
            dy = 0

        if dy == 0 or abs(dx) <= abs(dy):
            self.velocity = Vector(0, self.velocity.y)
            self.position += Vector(dx, 0)
        if dx == 0 or abs(dy) <= abs(dx):
            self.velocity = Vector(self.velocity.x, 0)
            self.position += Vector(0, dy)

        self._normalize()


class RectBlob(Blob):
    def __init__(self, width, height, color, **kwargs):
        self.image = Surface((width * PS.PPU, height * PS.PPU))
        self.image.fill(Color(color))
        super().__init__(**kwargs)


class ImageBlob(Blob):
    def __init__(self, file, **kwargs):
        self.image = pygame.image.load(file).convert_alpha()
        super().__init__(**kwargs)


class Platform(RectBlob):
    def __init__(self, **kwargs):
        super().__init__(color='blue', **kwargs)


class Player(RectBlob):
    def __init__(self, **kwargs):
        super().__init__(width=PS.BLOB_SIZE, height=PS.BLOB_SIZE,
                         color='white', **kwargs)
        self.jump_frames = 0

    def update(self):
        if self.jump_frames > 0:
            self.jump_frames -= 1
        else:
            self.velocity += PS.GRAVITY / GS.FPS
        super().update()

    def can_jump(self, platforms):
        self.position += Vector(0, 2) / PS.PPU
        self._normalize()
        n_platforms = len(pygame.sprite.spritecollide(
            self, platforms, False))
        self.position -= Vector(0, 2) / PS.PPU
        self._normalize()
        return n_platforms > 0

    def go_left(self):
        self.velocity = Vector(-PS.RUN_SPEED, self.velocity.y)

    def go_right(self):
        self.velocity = Vector(PS.RUN_SPEED, self.velocity.y)

    def jump(self):
        self.velocity = Vector(self.velocity.x, -PS.JUMP_SPEED)
        self.jump_frames = PS.JUMP_TIME * GS.FPS

    def stop_left(self):
        if self.velocity.x < 0:
            self.velocity = Vector(0, self.velocity.y)

    def stop_right(self):
        if self.velocity.x > 0:
            self.velocity = Vector(0, self.velocity.y)

    def stop_jump(self):
        self.jump_frames = 0


class Gem(ImageBlob):
    def __init__(self, note, winner=False, **kwargs):
        file = os.path.join('images', f'gem{note}.png')
        super().__init__(file=file, **kwargs)
        self.note = note
        self.winner = winner

        # Get sound for this note.
        sound_path = os.path.join("sounds", "long", f"{note}.wav")
        self.sound = pygame.mixer.Sound(sound_path)
