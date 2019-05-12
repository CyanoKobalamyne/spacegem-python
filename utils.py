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

