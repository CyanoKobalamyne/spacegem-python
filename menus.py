import pygame as pg
from pygame.locals import *
from utils import *
from spaceships import *
from platformer import NotePlatformerScene
from narratives import Narratives
import world1

class TitleScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.sfont = pg.font.SysFont('Monospace', 32)
        self.state = {"level_progress": [0,0,0], "num_levels": [0,0,0]}
        self.state["num_levels"][0] = len([attr for attr in dir(world1) if not attr.startswith('__')])
        self.state["num_levels"][1] = len(pickle.load(open("levels", "rb")))

    def render(self, screen):
        screen.fill((0, 0, 0))
        logo = get_image("./images/logo.png")
        screen.blit(logo, (50,100))
        text = self.sfont.render('Click anywhere to begin', True, (255, 255, 255))
        screen.blit(text, (180, 350))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                scene = LevelsScene(self.state)
                self.manager.go_to(NarrativeScene(Narratives.intro, self.state, scene))
            if e.type == KEYDOWN:
                if e.key == K_0:
                    self.state["level_progress"] = self.state["num_levels"]

class LevelsScene(Scene):

    def __init__(self, state):
        self.state = state
        self.bg = pg.image.load("./images/levels-background.png")

    def render(self, screen):
        screen.blit(self.bg, (0,0))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pg.Rect(50, 490, 200, 50).collidepoint(pos):
                    scene = World1Scene(self.state)
                    self.manager.go_to(NarrativeScene(Narratives.World1.intro, self.state, scene))
                elif pg.Rect(300, 490, 200, 50).collidepoint(pos):
                    scene = World2Scene(self.state)
                    self.manager.go_to(NarrativeScene(Narratives.World2.intro, self.state, scene))
                elif pg.Rect(550, 490, 200, 50).collidepoint(pos):
                    self.manager.go_to(World3Scene(self.state))


class World1Scene(Scene):
    def __init__(self, state):
        self.state = state
        self.font = pg.font.SysFont('Monospace', 70)
        self.back = BackButton()
        self.levelsquares = pg.sprite.Group()
        for i in range(self.state["num_levels"][0]):
            available = (i <= self.state["level_progress"][0])
            self.levelsquares.add(LevelSquare(50+150*i, 300, i, available))

    def render(self, screen):
        screen.fill((0, 0, 0))
        pg.draw.rect(screen, (255, 255, 255), Rect(250, 100, 300, 100), 5)
        text = self.font.render("Levels", True, (255, 255, 255))
        screen.blit(text, (275, 110))
        self.back.draw(screen)
        for ls in self.levelsquares:
            ls.draw(screen)

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                lvl = [l for l in self.levelsquares if l.rect.collidepoint(pos)]
                if len(lvl) > 0 and lvl[0].available:
                    level_state = {"world": 0,
                                   "level": lvl[0].level}
                    state = {**self.state, **level_state}
                    scene = NotePlatformerScene(state)
                    if len(Narratives.World1.levels[lvl[0].level]) > 0:
                        self.manager.go_to(NarrativeScene(Narratives.World1.levels[lvl[0].level], state, scene))
                    else:
                        self.manager.go_to(scene)
                elif self.back.rect.collidepoint(pos):
                    self.manager.go_to(LevelsScene(self.state))

class World2Scene(Scene):

    def __init__(self, state):
        self.state = state
        self.font = pg.font.SysFont('Monospace', 70)
        self.back = BackButton()
        self.levelsquares = pg.sprite.Group()
        for i in range(self.state["num_levels"][1]):
            available = (i <= self.state["level_progress"][1])
            self.levelsquares.add(LevelSquare(50+150*i, 300, i, available))

    def render(self, screen):
        screen.fill((0, 0, 0))
        pg.draw.rect(screen, (255,255,255), Rect(250,100,300,100), 5)
        text = self.font.render("Levels", True, (255, 255, 255))
        screen.blit(text, (275,110))
        self.back.draw(screen)
        for ls in self.levelsquares:
            ls.draw(screen)

    def update(self):
        pass

    def handle_events(self, events):
         for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                lvl = [l for l in self.levelsquares if l.rect.collidepoint(pos)]
                if len(lvl) > 0 and lvl[0].available:
                    level_state = {"world": 1,
                                   "level": lvl[0].level,
                                   "ship_num": None,
                                   "ships": None,
                                   "start_time": pg.time.get_ticks(),
                                   "curr_time": pg.time.get_ticks()}
                    state = {**self.state, **level_state}
                    scene = SpaceshipScene(state)
                    if len(Narratives.World2.levels[lvl[0].level]) > 0:
                        self.manager.go_to(NarrativeScene(Narratives.World2.levels[lvl[0].level], state, scene))
                    else:
                        self.manager.go_to(scene)
                elif self.back.rect.collidepoint(pos):
                    self.manager.go_to(LevelsScene(self.state))

class World3Scene(Scene):

    def __init__(self, state):
        self.state = state
        self.font = pg.font.SysFont('Monospace', 56)

    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('Unimplemented', True, (255, 255, 255))
        screen.blit(text1, (200, 50))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                self.manager.go_to(LevelsScene(self.state))

class TransitionScene(Scene):
    def __init__(self, message, color, state):
        super(TransitionScene, self).__init__()
        self.font = pg.font.SysFont('Monospace', 36)
        self.sfont = pg.font.SysFont('Monospace', 30)
        self.message = message
        self.color = color
        self.state = state

    def render(self, screen):
        screen.fill(self.color)
        text1 = self.font.render(self.message, True, (255, 255, 255))
        text2 = self.sfont.render('Click anywhere to continue', True, (255, 255, 255))
        screen.blit(text1, (200, 50))
        screen.blit(text2, (200, 350))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                if self.state["world"] == 0:
                    self.manager.go_to(World1Scene(self.state))
                elif self.state["world"] == 1:
                    self.manager.go_to(World2Scene(self.state))
                elif self.state["world"] == 2:
                    self.manager.go_to(World3Scene(self.state))

class WinScene(TransitionScene):
    def __init__(self, state):
        super(WinScene, self).__init__('You\'ve won this level', (50, 100, 50), state)

class LoseScene(TransitionScene):
    def __init__(self, state):
        super(LoseScene, self).__init__('You\'ve lost this level', (120, 30, 30), state)

class LevelSquare(pg.sprite.Sprite):
    def __init__(self, x, y, level, available):
        super().__init__()
        self.font = pg.font.SysFont('Monospace', 80)
        self.image = pg.Surface([100, 100])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.available = available
        if self.available:
            self.color = (255,255,255)
        else:
            self.color = (127,127,127)

    def draw(self, screen):
        pg.draw.rect(screen, self.color, self.rect, 5)
        text = self.font.render(str(self.level+1), True, self.color)
        screen.blit(text, (self.rect.x+25,self.rect.y+5))

class NarrativeScene(Scene):
    def __init__(self, texts, state, scene):
        super(NarrativeScene, self).__init__()
        self.font = pg.font.SysFont('Monospace', 32)
        self.texts = texts
        self.text_num = 0
        self.state = state
        self.scene = scene
        self.bg = pg.image.load("./images/narrative-background.png")

    def render(self, screen):
        screen.blit(self.bg, (0,0))
        self.drawText(screen, self.texts[self.text_num])

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pg.Rect(380, 500, 120, 50).collidepoint(pos):
                    self.text_num += 1
                elif pg.Rect(550, 500, 200, 50).collidepoint(pos):
                    self.text_num = len(self.texts)
                if self.text_num == len(self.texts):
                    self.manager.go_to(self.scene)

    def drawText(self, screen, text):
        rect = pg.Rect(50,70,700,450)
        y = rect.top
        lineSpacing = -2
        fontHeight = self.font.size("Tg")[1]

        while text:
            i = 1
            while self.font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1
            image = self.font.render(text[:i], True, (255,255,255))
            screen.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing
            text = text[i:]
        return text
