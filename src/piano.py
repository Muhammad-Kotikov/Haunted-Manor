# Mithilfe von https://www.youtube.com/watch?v=47c_1wOa2so&t=250s erstellt

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame
import notes as pl 

from pygame import mixer
from settings import Resolution
from tools import get_full_path, get_sprite, get_mouse_pos

### Piano Klasse
class Piano():
    #   Farben
    WHITE           = (255, 255, 255)
    BLACK           = (000, 000, 000)
    BORDER_COLOR    = (120, 0, 000)

    #   Spielspezifische Variablen
    LEFT_OCT            = 4
    RIGHT_OCT           = 5

    PIANO_NOTES         = pl.piano_notes
    WHITE_NOTES         = pl.white_notes
    BLACK_NOTES         = pl.black_notes
    BLACK_LABELS        = pl.black_labels

    SHOW_BORDER_DURATION = 60 * 2

    CORRECT_SEQUENCE    = ['D4', 'E4']

    #### Initialisierung der Klasse
    def __init__(self):
        #   Schriftarten
        self.BIG_FONT            = pygame.font.Font(None, 200)
        self.FONT                = pygame.font.Font(None, 48)
        self.SMALL_FONT          = pygame.font.Font(None, 16)
        self.REAL_SMALL_FONT     = pygame.font.Font(None, 10)

        #   Sounds    
        self.white_sounds        = [mixer.Sound(get_full_path(f'sounds/piano_notes/{note}.wav')) for note in pl.white_notes]
        self.black_sounds        = [mixer.Sound(get_full_path(f'sounds/piano_notes/{note}.wav')) for note in pl.black_notes]

        #   Image  
        self.sheet_music_image = get_sprite("sheet_music_image.png")

        #   Spielspezifische Variablen
        self.active_whites       = []
        self.active_blacks       = []
        self.played_notes        = []

        self.white_rects = []
        self.black_rects = []
        
        #   Bild skalieren, da es hier immer Probleme gab
        image_width, image_height   = self.sheet_music_image.get_size()
        available_height            = Resolution.HEIGHT - 300
        scale_factor                = available_height / image_height
        new_width                   = int(image_width * scale_factor)
        new_height                  = int(image_height * scale_factor)
        self.scaled_image           = pygame.transform.scale(self.sheet_music_image, (new_width, new_height))
        self.image_x                = (Resolution.WIDTH - new_width) // 2  
    
        self.image_y                = 0 
        self.exit = False

        #   Weiße Tasten 
        for i in range(52):
            rect = pygame.Rect(i * 25, Resolution.HEIGHT - 300, 25, 300)
            self.white_rects.append(rect)

        skip_count  = 0
        last_skip   = 2
        skip_track  = 2
        skip_count  = 0

        #   Schwarze Tasten
        for i in range(36):
            rect = pygame.Rect(23 + (i * 25) + (skip_count * 25), Resolution.HEIGHT - 300, 24, 200)

            skip_track += 1

            if last_skip == 2 and skip_track == 3:
                last_skip   = 3
                skip_track  = 0
                skip_count  += 1

            elif last_skip == 3 and skip_track == 2:
                last_skip   = 2
                skip_track  = 0
                skip_count  += 1

            self.black_rects.append(rect)
    
### Update-Methode   
    def update(self):

        self.decrement_timer()
        self.click_notes()

### Render-Methode   
    def render(self):

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.scaled_image, (self.image_x, self.image_y))
        self.draw_piano()
    
### Decrementtimer - Methode
    def decrement_timer(self):
        #   Timer für die Umrandung der geklickten Noten
        for index, played_note in enumerate(self.active_whites):
            played_note[1] -= 1
            if played_note[1] <= 0:
                self.active_whites.pop(index)

        for index, played_note in enumerate(self.active_blacks):
            played_note[1] -= 1
            if played_note[1] <= 0:
                self.active_blacks.pop(index)
    

    def click_notes(self):
        #   Klickverarbeitung und gibt die entsprechenden Noten aus
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit = True

            if not event.type == pygame.MOUSEBUTTONDOWN:
                return

            pos = get_mouse_pos()

            black_key = False
            for i, key in enumerate(self.black_rects):
                if key.collidepoint(pos):
                    self.black_sounds[i].play(0)
                    black_key = True
                    self.active_blacks.append([i, self.SHOW_BORDER_DURATION])
                    self.played_notes.append(self.BLACK_NOTES[i]) 
                    break

            if black_key:
                return 

            for i, key in enumerate(self.white_rects):
                if key.collidepoint(pos):
                    self.white_sounds[i].play(0)
                    self.active_whites.append([i, self.SHOW_BORDER_DURATION])
                    self.played_notes.append(self.WHITE_NOTES[i])
                    break
                
### Klavier zeichnen-Methode
    def draw_piano(self):
        #   Weiße Tasten
        for i in range(52):
            pygame.draw.rect(self.screen, self.WHITE, self.white_rects[i], 0, 5)
            pygame.draw.rect(self.screen, self.BLACK, self.white_rects[i], 1, 5)
            key_label = self.SMALL_FONT.render(self.WHITE_NOTES[i], True, self.BLACK)
            self.screen.blit(key_label, (self.white_rects[i].left + 3, Resolution.HEIGHT - 20))
        
        #   Umriss um gedrückte weiße Tasten
        for played in self.active_whites:
            note, _ = played
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.white_rects[note], 2, 2)

        #   Schwarze Tasten
        for i in range(36):
            pygame.draw.rect(self.screen, self.BLACK, self.black_rects[i], 0, 5)
            key_label = self.REAL_SMALL_FONT.render(self.BLACK_LABELS[i], True, self.WHITE)
            self.screen.blit(key_label, (self.black_rects[i].left + 2, Resolution.HEIGHT - 120))
        
        #   Umriss um gedrückte schwarze Tasten
        for played in self.active_blacks:
            note, _ = played
            pygame.draw.rect(self.screen, self.BORDER_COLOR, self.black_rects[note], 2, 2)