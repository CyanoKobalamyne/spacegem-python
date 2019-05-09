import pygame as pg
import random
 
# -- Global constants
 
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 128, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 204, 0)
TEAL = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (150, 0, 255)


GEM_COLORS = [RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, PURPLE, RED]
SEMITONE_MAP = [0, 2, 4, 5, 7, 9, 11, 12]
 
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Gems:

    def __init__(self):
        self.gems = pg.sprite.Group()
        for i in range(8):
            self.gems.add(Gem(60 + i*60, 450, i))

class Gem(pg.sprite.Sprite): 

    def __init__(self, x, y, tone):
        super().__init__()

        self.image = pg.Surface([40, 40])
        self.image.fill(GEM_COLORS[tone])
     
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.tone = tone

class TransmissionDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.update_signal()

    def update_signal(self, signal=[0, 0]):
        peak1 = SEMITONE_MAP[signal[0]]
        peak2 = SEMITONE_MAP[signal[1]]
        pointlist1 = [(75, 320), (125, 305-peak1*15), (175, 320)]
        pointlist2 = [(225, 320), (275, 305-peak2*15), (325, 320)]
        pg.draw.polygon(self.screen, BRIGHT_GREEN, pointlist1, 2)
        pg.draw.polygon(self.screen, BRIGHT_GREEN, pointlist2, 2)

class SoundDisplay:
    def __init__(self, screen, flag):
        self.screen = screen
        self.text_size = 50
        self.text_color = RED
        self.topleft_pos = (520, 20)
        self.font = pg.font.SysFont('Monospace', self.text_size)
        self.notes = []
        self.text = self.font.render("", True, self.text_color)
        self.text_rect = self.text.get_rect(topleft=self.topleft_pos)
        self.flag = flag

    def draw_peaks(self, note, signal_number):
        peak = SEMITONE_MAP[note]
        pointlist = [(475+150*signal_number, 320), 
            (525+150*signal_number, 305-peak*15), 
            (575+150*signal_number, 320)]
        pg.draw.polygon(self.screen, RED, pointlist, 3)

    def update_text(self, note, signal):
        correct = False
        if len(self.notes) == 0 or len(self.notes) == 2:
            self.notes = [note]
        elif len(self.notes) == 1:
            diff = abs(SEMITONE_MAP[note] - SEMITONE_MAP[self.notes[0]])
            if diff == SEMITONE_MAP[signal[1]]-SEMITONE_MAP[signal[0]]:
                self.flag.update_status(GREEN)
                correct = True
            else:
                self.flag.update_status(RED)
            self.notes.append(note)
        return correct

    def draw(self):
        if len(self.notes) > 0:
            self.draw_peaks(self.notes[0], 0)
        if len(self.notes) > 1:
            self.draw_peaks(self.notes[1], 1)

class ErrorFlag(pg.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pg.Surface([76, 76])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = 432
        self.rect.x = 612
        self.update_status()

    def update_status(self, color=BLACK):
        self.image.fill(color)

#can only take up to 2 notes
def play_notes(channel,notes):
    channel.play(pg.mixer.Sound("./sounds/"+str(notes[0])+".wav"))
    if len(notes) > 1:
        channel.queue(pg.mixer.Sound("./sounds/"+str(notes[1])+".wav"))

pg.init()
screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pg.display.set_caption('Test')

sprites = pg.sprite.Group()
flag = ErrorFlag()
sprites.add(flag)
transmission = TransmissionDisplay(screen)
sound = SoundDisplay(screen, flag)
gems = Gems()
signal = sorted([random.randint(0,7), random.randint(0, 7)])

pg.mixer.init()
channel = pg.mixer.find_channel()
play_notes(channel,signal)

bg = pg.image.load("./images/transmission-background.png")

done = False

while not done:
 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        elif event.type == pg.MOUSEBUTTONUP:
            pos = pg.mouse.get_pos()
            gem = [g for g in gems.gems if g.rect.collidepoint(pos)]
            if len(gem) > 0:
                #pg.mixer.Sound("./sounds/"+str(gem[0].tone)+".wav").play()
                play_notes(channel,[gem[0].tone])
                correct = sound.update_text(gem[0].tone, signal)
                if correct:
                    signal = sorted([random.randint(0,7), random.randint(0, 7)])
                    play_notes(channel,signal)
            elif pg.Rect(160, 340, 190, 38).collidepoint(pos):
                play_notes(channel,signal)

    screen.blit(bg, (0,0))
    gems.gems.draw(screen)
    transmission.update_signal(signal)
    sound.draw()
    sprites.draw(screen)
    pg.display.update()
 
pg.quit()
