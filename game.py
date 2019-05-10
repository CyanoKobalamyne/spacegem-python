import pygame as pg
from pygame.locals import *
import random

from utils import *
from interval import *
from menus import *
from spaceships import *

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

def main():
    pg.init()
    screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    pg.display.set_caption('Test')
    timer = pg.time.Clock()
    running = True

    manager = SceneManager(TitleScene())

    while running:
        timer.tick(60)

        if pg.event.get(QUIT):
            running = False
            return
        manager.scene.handle_events(pg.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pg.display.flip()

if __name__ == "__main__":
    main()
