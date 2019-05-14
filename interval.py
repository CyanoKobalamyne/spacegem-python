import pygame as pg
import random
from utils import *
import menus

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 204, 0)

SEMITONE_MAP = [0, 2, 4, 5, 7, 9, 11, 12]

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

        self.image = get_image("./images/gem"+ str(tone) +".png").subsurface(pg.Rect(0,0,56,58))

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.tone = tone


class IntervalScene(Scene):
    def __init__(self, signals, lose_time, state):
        super(IntervalScene, self).__init__()

        self.sprites = pg.sprite.Group()
        self.flag = ErrorFlag()
        self.timeremaining = TimeRemaining(lose_time)
        self.sprites.add(self.flag)
        self.sound = SoundDisplay(self.flag)
        self.gems = pg.sprite.Group()
        for i in range(8):
            if i not in state["broken"]:
                self.gems.add(Gem(52 + i*60, 440, i))
        self.signals = signals
        self.sound.signal = signals[0]
        self.interval_num = 0

        self.lose_time = lose_time
        self.state = state

        pg.mixer.init()
        self.gem_channel = pg.mixer.find_channel()
        self.sig_channel = pg.mixer.find_channel()
        self.play_notes(self.sig_channel,self.sound.signal)

        self.new_mouse_gem = False
        self.mouseover = 0

        self.bg = pg.image.load("./images/transmission-background.png")

    def render(self, screen):
        if pg.time.get_ticks() - self.state["curr_time"] > self.lose_time:
            self.manager.go_to(menus.LoseScene(self.state))
        screen.blit(self.bg, (0,0))
        self.gems.draw(screen)
        self.sound.draw(screen, self.state["disrupt"])
        self.sprites.draw(screen)
        self.timeremaining.draw(screen, self.lose_time-(pg.time.get_ticks() - self.state["curr_time"]))
        gem = self.mouse_gem()
        if len(gem) > 0 and (self.mouseover != gem[0].tone):
            self.mouseover = gem[0].tone
            self.new_mouse_gem = True
        elif len(gem) == 0 and self.mouseover >= 0:
            self.mouseover = -1
            self.gem_channel.stop()
        if self.new_mouse_gem:
            self.play_notes(self.gem_channel,[self.mouseover], long_note = True)
            self.new_mouse_gem = False


    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                gem = self.mouse_gem()
                if len(gem) > 0:
                    correct = self.sound.update_text(gem[0].tone)
                    if correct:
                        self.interval_num += 1
                        if self.interval_num < len(self.signals):
                            self.sound.signal = self.signals[self.interval_num]
                        else:
                            self.state["ships"][self.state["ship_num"]] = False
                            self.state["curr_time"] = pg.time.get_ticks()
                            from spaceships import SpaceshipScene
                            self.manager.go_to(SpaceshipScene(self.state))
                        self.play_notes(self.sig_channel,self.sound.signal)
                elif pg.Rect(160, 340, 190, 38).collidepoint(pos):
                    self.play_notes(self.sig_channel,self.sound.signal)


    def mouse_gem(self):
        pos = pg.mouse.get_pos()
        gem = [g for g in self.gems if g.rect.collidepoint(pos)]
        return gem

    #can only take up to 2 notes
    def play_notes(self, channel, notes, long_note = False):
        if long_note:
            path = "./sounds/long/"
        else:
            path = "./sounds/short/"
        channel.play(pg.mixer.Sound(path+str(notes[0])+".wav"))
        if len(notes) > 1:
            channel.queue(pg.mixer.Sound(path+str(notes[1])+".wav"))

class SoundDisplay:
    def __init__(self, flag):
        self.notes = []
        self.flag = flag
        self.signal = [0,0]

    def draw_peaks(self, note, signal_number, color, screen):
        peak = SEMITONE_MAP[note]
        pointlist = [(75+100*signal_number, 320),
            (125+100*signal_number, 305-peak*15),
            (175+100*signal_number, 320)]
        pg.draw.polygon(screen, color, pointlist, 3)

    def update_text(self, note):
        correct = False
        if len(self.notes) == 0 or len(self.notes) == 2:
            self.flag.update_status(BLACK)
            self.notes = [note]
        elif len(self.notes) == 1:
            diff = abs(SEMITONE_MAP[note] - SEMITONE_MAP[self.notes[0]])
            if diff == SEMITONE_MAP[self.signal[1]]-SEMITONE_MAP[self.signal[0]]:
                self.flag.update_status(GREEN)
                correct = True
            else:
                self.flag.update_status(RED)
            self.notes.append(note)
            self.complete_time = pg.time.get_ticks()
        return correct

    def draw(self, screen, disrupt):
        if len(self.notes) == 2 and pg.time.get_ticks() - self.complete_time > 1000:
            self.flag.update_status(BLACK)
            self.notes = []
        if not disrupt:
            self.draw_peaks(self.signal[0], 0, BLUE, screen)
            self.draw_peaks(self.signal[1], 1.5, BLUE, screen)
        if len(self.notes) > 0:
            self.draw_peaks(self.notes[0], 4, BLUE, screen)
        if len(self.notes) > 1:
            self.draw_peaks(self.notes[1], 5.5, BLUE, screen)

class ErrorFlag(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([76, 76])
        #self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = 432
        self.rect.x = 612
        #self.update_status()

    def update_status(self, color):
        self.image.fill(color)

class TimeRemaining:
    def __init__(self, total_time):
        self.total_time = total_time
        self.remaining_time = total_time

    def draw(self, screen, remaining_time):
        width = (remaining_time/self.total_time)*370
        if width > 74:
            color = GREEN
        else:
            color = RED
        pg.draw.rect(screen, color, pg.Rect(310, 540, width, 20))

