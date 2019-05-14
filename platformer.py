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
import pygame.transform
from pygame import Color, Surface
from pygame.sprite import Group, Sprite

import menus
from setup import GameSettings as GS
from setup import PlatformerSettings as PS
from utils import Button, HorizontalScrollingGroup, Scene, TextBox, Vector
import world1


class NotePlatformerScene(Scene):
    def __init__(self, state):
        level = getattr(world1, f"Level_{state['level'] + 1}")

        self.state = state
        self.player = Player(position=Vector(*level.player))

        self.platforms = Group()
        self.gems = Group()
        level_width = PS.PPU * (
            max(map(lambda p: p[0] + p[2], level.platforms)) + PS.BLOB_SIZE)
        self.blobs = HorizontalScrollingGroup(
            self.player, (GS.SCREEN_WIDTH, GS.SCREEN_HEIGHT),
            (level_width, GS.SCREEN_HEIGHT), PS.SCROLL_MARGIN * PS.PPU)

        for x, y, width in level.platforms:
            platform = Platform(width=width, position=Vector(x, y))
            self.blobs.add(platform)
            self.platforms.add(platform)
        for x, y, note, winner in level.gems:
            gem = Gem(note, winner=winner, position=Vector(x, y))
            self.blobs.add(gem)
            self.gems.add(gem)
            if winner:
                goal_path = os.path.join("sounds", "long", f"{note}.wav")
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

        if self.player.rect.bottom > GS.SCREEN_HEIGHT:
            self.quit(win=False)

        # Play sound near gems.
        for gem in self.gems:
            self.player.listen_to(gem)

        # Handle collisions with gems.
        for gem in pygame.sprite.spritecollide(
                self.player, self.gems, False):
            # End condition.
            self.quit(win=gem.winner)

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

    def quit(self, win):
        for gem in self.gems:
            gem.sound.stop()
        if win:
            self.state["level_progress"][self.state["world"]] = (
                self.state["level"] + 1)
        next_scene = menus.WinScene if win else menus.LoseScene
        self.manager.go_to(next_scene(self.state))


class Blob(Sprite):
    def __init__(self, position, velocity=Vector(0, 0)):
        super().__init__()
        self.velocity = velocity * PS.PPU
        self.rect = self.image.get_rect()
        self.rect.move_ip(position * PS.PPU)

    def update(self):
        self.rect.x += self.velocity.x / GS.FPS
        self.rect.y += self.velocity.y / GS.FPS

    def collide(self, other):
        if self.velocity.x > 0:
            dx = other.rect.left - self.rect.right
        elif self.velocity.x < 0:
            dx = other.rect.right - self.rect.left
        else:
            dx = None

        if self.velocity.y > 0:
            dy = other.rect.top - self.rect.bottom
        elif self.velocity.y < 0:
            dy = self.rect.top - other.rect.bottom
        else:
            dy = None

        if dx is not None and (dy is None or abs(dx) <= abs(dy)):
            self.velocity = Vector(0, self.velocity.y)
            self.rect.x += dx
        if dy is not None and (dx is None or abs(dy) <= abs(dx)):
            self.velocity = Vector(self.velocity.x, 0)
            self.rect.y += dy

    @staticmethod
    def distance(blob1, blob2):
        p1 = Vector(*blob1.rect.center)
        p2 = Vector(*blob2.rect.center)
        return abs(p1 - p2) / PS.PPU


class RectBlob(Blob):
    def __init__(self, width, height, color, **kwargs):
        self.image = Surface((width * PS.PPU, height * PS.PPU))
        self.image.fill(color)
        super().__init__(**kwargs)


class ImageBlob(Blob):
    def __init__(self, file, **kwargs):
        self.image = pygame.image.load(file).convert_alpha()
        super().__init__(**kwargs)


class Platform(RectBlob):
    def __init__(self, **kwargs):
        super().__init__(height=PS.PLATFORM_HEIGHT, color=PS.PLATFORM_COLOR,
                         **kwargs)


class Player(ImageBlob):
    def __init__(self, **kwargs):
        super().__init__(file=os.path.join("images", "player.png"), **kwargs)
        self.img_normal = self.image
        self.img_reflected = pygame.transform.flip(self.image, True, False)
        self.jump_frames = 0

    def update(self):
        # Handle jumping and gravity.
        if self.jump_frames > 0:
            self.jump_frames -= 1
        else:
            self.velocity += PS.GRAVITY * PS.PPU / GS.FPS

        # Handle orientation.
        if self.velocity.x > 0:
            self.image = self.img_normal
        elif self.velocity.x < 0:
            self.image = self.img_reflected

        super().update()

    def can_jump(self, platforms):
        self.rect.y += 2
        n_platforms = len(pygame.sprite.spritecollide(
            self, platforms, False))
        self.rect.y -= 2
        return n_platforms > 0

    def go_left(self):
        self.velocity = Vector(-PS.RUN_SPEED * PS.PPU, self.velocity.y)

    def go_right(self):
        self.velocity = Vector(PS.RUN_SPEED * PS.PPU, self.velocity.y)

    def jump(self):
        self.velocity = Vector(self.velocity.x, -PS.JUMP_SPEED * PS.PPU)
        self.jump_frames = PS.JUMP_TIME * GS.FPS

    def stop_left(self):
        if self.velocity.x < 0:
            self.velocity = Vector(0, self.velocity.y)

    def stop_right(self):
        if self.velocity.x > 0:
            self.velocity = Vector(0, self.velocity.y)

    def stop_jump(self):
        self.jump_frames = 0

    def listen_to(self, gem):
        distance = Blob.distance(self, gem) - PS.BLOB_SIZE
        if distance <= PS.SOUND_RADIUS:
            if not gem.playing:
                gem.sound.play(loops=-1)
                gem.playing = True
            vol_ratio = 1 - distance / PS.SOUND_RADIUS
            gem.sound.set_volume(vol_ratio)
        else:
            gem.sound.stop()
            gem.playing = False


class Gem(ImageBlob):
    def __init__(self, note, winner=False, **kwargs):
        file = os.path.join('images', f'gem{note}.png')
        super().__init__(file=file, **kwargs)
        self.note = note
        self.winner = winner
        self.playing = False

        # Get sound for this note.
        sound_path = os.path.join("sounds", "short", f"{note}.wav")
        self.sound = pygame.mixer.Sound(sound_path)
