import pygame as pg
from pygame.locals import *
from utils import *
from spaceships import *
from platformer import NotePlatformerScene

class TitleScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.font = pg.font.SysFont('Monospace', 56)
        self.sfont = pg.font.SysFont('Monospace', 32)
        self.state = {"level_progress": [0,0,0], "num_levels": [0,0,0]}
        # TODO: load number of levels from data for world 1!!
        self.state["num_levels"][1] = len(pickle.load(open("levels", "rb")))

    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('SPACEGEM', True, (255, 255, 255))
        text2 = self.sfont.render('Click anywhere to begin', True, (255, 255, 255))
        screen.blit(text1, (200, 50))
        screen.blit(text2, (200, 350))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                self.manager.go_to(LevelsScene(self.state))

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
                    self.manager.go_to(World1Scene(self.state))
                elif pg.Rect(300, 490, 200, 50).collidepoint(pos):
                    self.manager.go_to(World2Scene(self.state))
                elif pg.Rect(550, 490, 200, 50).collidepoint(pos):
                    self.manager.go_to(World3Scene(self.state))


class World1Scene(Scene):
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
                    level_state = {"world": 1,
                                   "level": lvl[0].level}
                    state = {**self.state, **level_state}
                    self.manager.go_to(NotePlatformerScene(state))
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
                    self.manager.go_to(SpaceshipScene(state))
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
        super(WinScene, self).__init__('You\'ve won this level', (50, 200, 50), state)

class LoseScene(TransitionScene):
    def __init__(self, state):
        super(LoseScene, self).__init__('You\'ve lost this level', (200, 50, 50), state)

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
