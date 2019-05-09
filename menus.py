import pygame as pg
from pygame.locals import *
from utils import *
from interval import *

class TitleScene(Scene):

    def __init__(self):
        super(TitleScene, self).__init__()
        self.font = pg.font.SysFont('Arial', 56)
        self.sfont = pg.font.SysFont('Arial', 32)

    def render(self, screen):
        # ugly! 
        screen.fill((0, 200, 0))
        text1 = self.font.render('Crazy Game', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to start <', True, (255, 255, 255))
        screen.blit(text1, (200, 50))
        screen.blit(text2, (200, 350))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.manager.go_to(IntervalScene()) # can input something to init for which intervals
