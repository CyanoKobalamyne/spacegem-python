import pygame as pg 
import random
from utils import *

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

        self.image = pg.Surface([40, 40])
        self.image.fill(GEM_COLORS[tone])
     
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.tone = tone


class IntervalScene(Scene):
    def __init__(self):
        super(IntervalScene, self).__init__()
       
        self.sprites = pg.sprite.Group()
        self.flag = ErrorFlag()
        self.sprites.add(self.flag)
        self.sound = SoundDisplay(self.flag)
        self.gems = pg.sprite.Group()
        for i in range(8):
            self.gems.add(Gem(60 + i*60, 450, i))
        self.sound.signal = sorted([random.randint(0,7), random.randint(0, 7)])
        
        pg.mixer.init()
        self.channel = pg.mixer.find_channel()
        self.play_notes(self.channel,self.sound.signal)
        
        self.bg = pg.image.load("./images/transmission-background.png")

    def render(self, screen):
        screen.blit(self.bg, (0,0))
        self.gems.draw(screen)
        self.sound.draw(screen)
        self.sprites.draw(screen)

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                gem = [g for g in self.gems if g.rect.collidepoint(pos)]
                if len(gem) > 0:
                    #pg.mixer.Sound("./sounds/"+str(gem[0].tone)+".wav").play()
                    self.play_notes(self.channel,[gem[0].tone])
                    correct = self.sound.update_text(gem[0].tone)
                    if correct:
                        self.sound.signal = sorted([random.randint(0,7), random.randint(0, 7)])
                        self.play_notes(self.channel,self.sound.signal)
                elif pg.Rect(160, 340, 190, 38).collidepoint(pos):
                    self.play_notes(self.channel,self.sound.signal)
    
    # make this be the method that happens when the user finishes the interval puzzle
    def exit(self): 
        pass

    #can only take up to 2 notes
    def play_notes(self, channel, notes):
        channel.play(pg.mixer.Sound("./sounds/"+str(notes[0])+".wav"))
        if len(notes) > 1:
            channel.queue(pg.mixer.Sound("./sounds/"+str(notes[1])+".wav"))

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
            self.notes = [note]
        elif len(self.notes) == 1:
            diff = abs(SEMITONE_MAP[note] - SEMITONE_MAP[self.notes[0]])
            if diff == SEMITONE_MAP[self.signal[1]]-SEMITONE_MAP[self.signal[0]]:
                self.flag.update_status(GREEN)
                correct = True
            else:
                self.flag.update_status(RED)
            self.notes.append(note)
        return correct

    def draw(self, screen):
        self.draw_peaks(self.signal[0], 0, BRIGHT_GREEN, screen)
        self.draw_peaks(self.signal[1], 1.5, BRIGHT_GREEN, screen)
        if len(self.notes) > 0:
            self.draw_peaks(self.notes[0], 4, RED, screen)
        if len(self.notes) > 1:
            self.draw_peaks(self.notes[1], 5.5, RED, screen)

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
