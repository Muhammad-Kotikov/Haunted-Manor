# Mithilfe von https://www.youtube.com/watch?v=47c_1wOa2so&t=250s erstellt

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame
import piano_lists as pl
from pygame import mixer
import time

### Screen-Einstellungen
WIDTH       = 52 * 35
HEIGHT      = 800
SCREEN      = pygame.display.set_mode([WIDTH, HEIGHT])
FPS         = 60

### Pygame initialisieren
pygame.init()
pygame.display.set_caption("Piano")
pygame.mixer.set_num_channels(50)

####        Wie kann ich ein Pygame-Fenster in einem bereits vorhandenen Fenster öffnen?

### Clock-Objekt
CLOCK       = pygame.time.Clock()

### Farben
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (150, 150, 150)  
GREEN       = (0,0, 255)

### Schriftarten
BIG_FONT            = pygame.font.Font(None, 200)
FONT                = pygame.font.Font(None, 48)
SMALL_FONT          = pygame.font.Font(None, 16)
REAL_SMALL_FONT     = pygame.font.Font(None, 10)

##  Spielspezifische Vorbereitung
### Sound-files laden
white_sounds        = [mixer.Sound(f'/Users/sidney/Documents/Studium/WS 24_25/PROG2/Haunted-Manor/Rätsel/04_Piano/notes/{note}.wav') for note in pl.white_notes]
black_sounds        = [mixer.Sound(f'/Users/sidney/Documents/Studium/WS 24_25/PROG2/Haunted-Manor/Rätsel/04_Piano/notes/{note}.wav') for note in pl.black_notes]

### Notenblatt laden
sheet_music_image   = pygame.image.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Haunted-Manor/Rätsel/04_Piano/Unknown-1.png')

### Variablen
active_whites       = []
active_blacks       = []
left_oct            = 4
right_oct           = 5

piano_notes         = pl.piano_notes
white_notes         = pl.white_notes
black_notes         = pl.black_notes
black_labels        = pl.black_labels

correct_sequence    = ['D4', 'E4']
played_notes        = []

### Funktionen
####Piano darstellen
def draw_piano(whites, blacks):
    white_rects = []
    
    # Weiße Tasten
    for i in range(52):
        rect = pygame.draw.rect(SCREEN, WHITE , [i * 35, HEIGHT - 300, 35, 300], 0, 2)
        white_rects.append(rect)
        pygame.draw.rect(SCREEN, BLACK, [i * 35, HEIGHT - 300, 35, 300], 2, 2)
        key_label = SMALL_FONT.render(white_notes[i], True, BLACK)
        SCREEN.blit(key_label, (i * 35 + 3, HEIGHT - 20))

    skip_count  = 0
    last_skip   = 2
    skip_track  = 2
    skip_count  = 0
    black_rects = []

    # Schwarze Tasten
    for i in range(36):
        rect = pygame.draw.rect(SCREEN, BLACK, [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200], 0, 2)
        for q in range(len(blacks)):
            if blacks[q][0] == i:
                if blacks[q][1] > 0:
                    pygame.draw.rect(SCREEN, GREEN , [23 + (i * 35) + (skip_count * 35), HEIGHT - 300, 24, 200], 2, 2)
                    blacks[q][1] -= 1

        key_label = REAL_SMALL_FONT.render(black_labels[i], True, WHITE)
        SCREEN.blit(key_label, (25 + (i * 35) + (skip_count * 35), HEIGHT - 120))
        black_rects.append(rect)

        skip_track += 1

        if last_skip == 2 and skip_track == 3:
            last_skip   = 3
            skip_track  = 0
            skip_count  += 1

        elif last_skip == 3 and skip_track == 2:
            last_skip   = 2
            skip_track  = 0
            skip_count  += 1

    for i in range(len(whites)):
        if whites[i][1] > 0:
            j = whites[i][0]
            whites[i][1] -= 1
            pygame.draw.rect(SCREEN, GREEN, [j * 35, HEIGHT - 100, 35, 100], 2, 2)

    return white_rects, black_rects, whites, blacks

####Notenblatt abbilden
def draw_sheet_music():
    image_width, image_height = sheet_music_image.get_size()
    available_height    = HEIGHT - 300
    scale_factor        = available_height / image_height
    new_width           = int(image_width * scale_factor)
    new_height          = int(image_height * scale_factor)
    scaled_image        = pygame.transform.scale(sheet_music_image, (new_width, new_height))
    image_x             = (WIDTH - new_width) // 2  
    image_y             = 0 

    SCREEN.fill(GRAY)
    SCREEN.blit(scaled_image, (image_x, image_y))

####Gewinn-Nachricht
def winning_message():
    global run

    pygame.time.delay(2000)
    SCREEN.fill(BLACK)
    winning_text = SMALL_FONT.render("Congratulations!", True, WHITE)
    text_rect = winning_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(winning_text, text_rect)
    pygame.display.flip()
    pygame.time.delay(5000)
    run = False

def draw_border():
    if not game_over:  
        for note in played_notes:
            if note in white_notes:
                note_index = white_notes.index(note)
                pygame.draw.rect(SCREEN, GREEN, [note_index * 35, HEIGHT - 100, 35, 100], 2, 2)
            elif note in black_notes:
                note_index = black_notes.index(note)
                pygame.draw.rect(SCREEN, GREEN, [23 + (note_index * 35), HEIGHT - 300, 24, 200], 2, 2)

#####################################################################################################################################################

# Game loop
running     = True
start_time  = None
game_over   = False
waiting_for_congratulations = False

##  Wait-Phase
while running:
    CLOCK.tick(FPS)
    draw_sheet_music()
    white_keys, black_keys, active_whites, active_blacks = draw_piano(active_whites, active_blacks)

##  Input-Phase
    for event in pygame.event.get():
        # Pygame quitten
        if event.type == pygame.QUIT:
            run = False

        # Piano-Taste auswählen
        if event.type == pygame.MOUSEBUTTONDOWN:
            black_key = False
            for i, key in enumerate(black_keys):
                if key.collidepoint(event.pos):
                    black_sounds[i].play(0)
                    black_key = True
                    active_blacks.append([i, 30])
                    played_notes.append(black_notes[i]) 
                    break  

            for i, key in enumerate(white_keys):
                if key.collidepoint(event.pos) and not black_key:
                    white_sounds[i].play(0)
                    active_whites.append([i, 30])
                    played_notes.append(white_notes[i])
                    break
    
    # Liste leeren
    if len(played_notes) > len(correct_sequence):
        played_notes = [] 

    for i in range(len(correct_sequence)):
        if i < len(played_notes) and played_notes[i] != correct_sequence[i]:
            played_notes = [] 
            print("Incorrect note played. Resetting sequence.")
            break
    
    # Auf korrekte Sequenz prüfen
    if played_notes == correct_sequence and not game_over:
        game_over = True
        winning_message()

    draw_border()

    pygame.display.update()

##  Double-Buffering
    pygame.display.flip()

#   Pygame schließen
pygame.quit()
