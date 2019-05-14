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


class Button:
    def __init__(self, text, position, padding):
        font = pygame.font.SysFont('Monospace', 30)
        size = Vector(*font.size(text)) + 2 * Vector(*padding)
        self.text = font.render(text, True, (255, 255, 255))
        self.rect = Rect(position, size)
        self.text_pos = Vector(*position) + Vector(*padding)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3)
        screen.blit(self.text, self.text_pos)


class BackButton(Button):
    def __init__(self):
        super().__init__("Back", Vector(50, 50), Vector(10, 5))


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


class TextBox:
    def __init__(self, text, bgcolor, max_size, style):
        font = pygame.font.SysFont(
            style["font"]["family"], style["font"]["size"])
        font_height = font.size("Tg")[1]
        line_spacing = style["paragraph"]["spacing"]
        color = style["font"]["color"]
        margin = style["text"]["margin"]
        width, max_height = max_size

        paragraphs = text.split('\n')
        lines = []
        for p in paragraphs:
            p_lines, _ = self._split_text(
                p, font, width, font_height, line_spacing, max_height)
            print(p_lines)
            lines.extend(p_lines)
            lines.append('')
        lines.pop()  # remove last extra line.

        height = len(lines) * (font_height + line_spacing) - line_spacing
        size = Vector(width, height)
        self.image = Surface(size + 2 * margin)
        self.image.fill(bgcolor)
        offset = Vector(*margin)
        for line in lines:
            text_image = font.render(line, True, color, bgcolor)
            text_image.set_colorkey(bgcolor)
            self.image.blit(text_image, offset)
            offset += Vector(0, font_height + line_spacing)

        self.rect = self.image.get_rect()

    def draw(self, screen, offset=None):
        if offset is None:
            offset = Vector(*screen.get_size()) / 2
            offset -= Vector(*self.image.get_size()) / 2
        screen.blit(self.image, offset)
        self.rect = self.image.get_rect()
        self.rect.move_ip(*offset)

    @staticmethod
    def _split_text(text, font, line_width, font_height, line_spacing,
                    max_height=float('inf')):
        lines = []
        height = 0
        while text:
            # Determine if the row of text will be outside our area
            if height + font_height > max_height:
                break

            # Determine last character that fits.
            for i in range(len(text)):
                if font.size(text[:i + 1])[0] > line_width:
                    break
            else:
                i += 1

            # Adjust to last word.
            if i < len(text):
                try:
                    # Wrap last word.
                    line_end = text.rindex(" ", 0, i)
                    next_start = line_end + 1
                except ValueError:
                    # Very long word overflowing line.
                    line_end = i
                    next_start = i
            else:
                # Remaining text shorter than line.
                line_end = i
                next_start = i

            # Remove this line.
            lines.append(text[:line_end])
            text = text[next_start:]

            height += font_height + line_spacing

        return lines, text


def get_image(file):
    image = pygame.image.load(file).convert_alpha()
    return image
