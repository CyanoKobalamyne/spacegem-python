import pygame as pg
from pygame.locals import *
from utils import *
from spaceships import *

class TitleScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.font = pg.font.SysFont('Monospace', 56)
        self.sfont = pg.font.SysFont('Monospace', 32)

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
                self.manager.go_to(LevelsScene())

class LevelsScene(Scene):

    def __init__(self):
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
                    self.manager.go_to(World1Scene())
                elif pg.Rect(300, 490, 200, 50).collidepoint(pos):
                    self.manager.go_to(World2Scene())
                elif pg.Rect(550, 490, 200, 50).collidepoint(pos):
                    self.manager.go_to(World3Scene())

class World1Scene(Scene):

    def __init__(self):
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
                self.manager.go_to(LevelsScene())

class World2Scene(Scene):

    def __init__(self):
        self.bg = pg.image.load("./images/world2.png")

    def render(self, screen):
        screen.blit(self.bg, (0,0))

    def update(self):
        pass

    def handle_events(self, events):
         for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                if pg.Rect(50, 300, 100, 100).collidepoint((pos[0] % 150, pos[1])):
                    state = {"level": pos[0] // 150,
                             "ship_num": None,
                             "ships": None,
                             "start_time": pg.time.get_ticks(),
                             "curr_time": pg.time.get_ticks()}
                    print(pos[0] //150)
                    self.manager.go_to(SpaceshipScene(state))

class World3Scene(Scene):

    def __init__(self):
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
                self.manager.go_to(LevelsScene())


class LoseScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.font = pg.font.SysFont('Arial', 56)
        self.sfont = pg.font.SysFont('Arial', 32)

    def render(self, screen):
        # ugly!
        screen.fill((200, 50, 50))
        text1 = self.font.render('You\'ve lost this level', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to continue <', True, (255, 255, 255))
        screen.blit(text1, (200, 50))
        screen.blit(text2, (200, 350))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.manager.go_to(SpaceshipScene()) # can input something to init for which intervals
