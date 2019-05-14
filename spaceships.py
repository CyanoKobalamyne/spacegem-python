import pygame as pg
from pygame.locals import *
import random
import pickle
from utils import *
import interval
import menus
from setup import GameSettings as Settings

BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 204, 0)

LEVELS = pickle.load(open("levels", "rb"))

class SpaceshipScene(Scene):
    def __init__(self, state):
        super(SpaceshipScene, self).__init__()
        self.state = state
        self.back = BackButton()
        self.level = LEVELS[state["level"]]
        if self.state["ships"] == None:
            self.state["ships"] = [True]*len(self.level)
        self.spaceships = pg.sprite.Group()
        time = self.state["curr_time"] - self.state["start_time"]
        for i in range(len(self.level)):
            if self.state["ships"][i]:
                disrupt = "disrupt" in self.level[i]
                broken = self.level[i]["broken"] if "broken" in self.level[i] else {}
                self.spaceships.add(Spaceship(self.level[i], time, i, disrupt, broken))

        self.bg = pg.image.load("./images/space-background.png")

    def render(self, screen):
        lose = [s for s in self.spaceships if s.rect.x < 100]
        if len(lose) > 0:
            self.manager.go_to(menus.LoseScene(self.state))
        if sum(self.state["ships"]) == 0:
            self.state["level_progress"][self.state["world"]] = self.state["level"] + 1
            self.manager.go_to(menus.WinScene(self.state))
        screen.blit(self.bg, (0,0))
        self.back.draw(screen)
        self.spaceships.draw(screen)

    def update(self):
        self.spaceships.update()

    def handle_events(self, events):
        for e in events:
            if e.type == MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                ship = [s for s in self.spaceships if s.rect.collidepoint(pos)]
                if len(ship) > 0:
                    self.state["ship_num"] = ship[0].num
                    self.state["curr_time"] = pg.time.get_ticks()
                    self.state["disrupt"] = ship[0].disrupt
                    self.state["broken"] = ship[0].broken
                    self.manager.go_to(interval.IntervalScene(ship[0].signals, ship[0].lose_time(), self.state))
                elif self.back.rect.collidepoint(pos):
                    self.manager.go_to(menus.World2Scene(self.state))

class Spaceship(pg.sprite.Sprite):
    def __init__(self, ship, time, num, disrupt=False, broken={}):
        super().__init__()
        self.signals = ship["signals"]
        self.num = num
        self.image = pg.Surface([40, 40])
        self.image = get_image("./images/enemy_in_ship.png")
        self.rect = self.image.get_rect()
        self.cycles = 0
        self.limit = 4
        self.rect.x = ship["x"] - time/1000*Settings.FPS/self.limit
        self.rect.y = ship["y"]
        self.disrupt = disrupt
        self.broken = broken
        if disrupt:
            pg.draw.rect(self.image, (0, 255, 127), pg.Rect(0,0,80,56), 3)
        if len(broken)>0:
            pg.draw.polygon(self.image, (255,0,0), [(1,6),(20,12),(1,18)], 3)

    def update(self):
        self.cycles += 1
        if self.cycles == self.limit:
            self.cycles = 0
            self.rect.x -= 1

    def lose_time(self):
        return (self.rect.x - 100)/(Settings.FPS/self.limit/1000)
