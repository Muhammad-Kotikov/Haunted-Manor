#   Mithilfe von: https://www.youtube.com/watch?v=IzsX89ZYGT0&t=625s erstellt

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import random
import pygame

### Screen-Einstellungen
WIDTH       = 800
HEIGHT      = 875
SCREEN      = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN + pygame.SCALED)
FPS         = 60

##  Pygame initialisieren
pygame.init()
pygame.display.set_caption('Memory')

####        Wie kann ich ein Pygame-Fenster in einem bereits vorhandenen Fenster öffnen?

##  Clock-Objekt
CLOCK       = pygame.time.Clock()

### Farben
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (128, 128, 128)
RED         = (255, 0, 0)

### Schriftarten
FONT        = pygame.font.Font(None, 100)
SMALL_FONT  = pygame.font.Font(None, 75)

##  Spielspezifische Vorbereitung
ROWS            = 6
COLS            = 6

piece_width     = WIDTH // COLS
piece_height    = (HEIGHT - 75) // ROWS

print(piece_width, piece_height)

options_list    = []
spaces_list     = []
used_pieces     = []
correct_matrix  = [[0] * COLS for _ in range(ROWS)]

reveal_timer    = 0  
game_timer      = 120 * 1000
start_time      = pygame.time.get_ticks()

first_guess     = False
second_guess    = False

first_guess_number  = 0
second_guess_number = 0

matches         = 0
game_over       = False
minigame_win    = 0

### Funktionen
####Hintergrund darstellen
def draw_background():
    top_menu    = pygame.draw.rect(SCREEN, BLACK, [0, 0, WIDTH, 75])
    board_space = pygame.draw.rect(SCREEN, GRAY, [0, 75, WIDTH, HEIGHT])

####Zahlen für das Bord generieren
def generate_board():
    global options_list
    global spaces_list
    global used_pieces

    for item in range(ROWS * COLS // 2):
        options_list.append(item)

    for item in range(ROWS * COLS):
        piece = options_list[random.randint(0, (len(options_list)-1))]
        spaces_list.append(piece)

        if piece in used_pieces:
            used_pieces.remove(piece)
            options_list.remove(piece)
        else:
            used_pieces.append(piece)


####Spiel darstellen (Karten aufdecken, entferenen, ...)
def draw_board():
    for i in range(COLS):
        for j in range(ROWS):
            x = i * piece_width
            y = j * piece_height

            # Zeichne die weißen Karten
            if correct_matrix[j][i] == 0: 
                piece = pygame.draw.rect(SCREEN, WHITE, [x + 5, y + 80, piece_width -10, piece_height - 10],0, 4)

            # Text auf den Karten darstellen
            elif correct_matrix[j][i] == 1: 
                piece_text = FONT.render(str(spaces_list[i + j * COLS]), True, GRAY)
                SCREEN.blit(piece_text, (x + 5 + (piece_width - 10) // 2 - piece_text.get_width() // 2, y + 80 + (piece_height - 10) // 2 - piece_text.get_height() // 2))
            
            # Karten entfernen
            elif correct_matrix[j][i] == 2:  
                continue 

            # Karten aufdecken, wenn sie ausgewählt wurden
            if (first_guess and first_guess_number == i + j * COLS) or (second_guess and second_guess_number == i + j * COLS):
                piece_text = FONT.render(str(spaces_list[i + j * COLS]), True, GRAY)
                SCREEN.blit(piece_text, (x + 5 + (piece_width - 10) // 2 - piece_text.get_width() // 2, y + 80 + (piece_height - 10) // 2 - piece_text.get_height() // 2))

####Spielzüge überprüfen
def check_guesses(first, second):
    global correct_matrix, matches 
    if spaces_list[first] == spaces_list[second]:
        col1, row1 = first % COLS, first // COLS
        col2, row2 = second % COLS, second // COLS
        correct_matrix[row1][col1] = correct_matrix[row2][col2] = 2  
        return True
    else:
        return False

####Timer darstellen
def draw_timer():
    global game_timer
    global running
    passed_time = pygame.time.get_ticks() - start_time
    remaining_time = game_timer - passed_time
    
    if remaining_time < 0:
        remaining_time = 0
        game_over = True
        gameover_text = FONT.render("Game Over", True, RED)
        gameover_rect = pygame.draw.rect(SCREEN, BLACK, [WIDTH//2 - 500//2, HEIGHT // 2 - 75, 500, 200])
        SCREEN.blit(gameover_text, (WIDTH // 2 - gameover_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()
        pygame.time.delay(3000)  

        running = False

    minutes = remaining_time // 60000
    seconds = (remaining_time % 60000) // 1000

    timer_text = f"{minutes:02}:{seconds:02}"
    timer_surface = SMALL_FONT.render(timer_text, True, WHITE)
    SCREEN.blit(timer_surface, (WIDTH // 2 - timer_surface.get_width() // 2, 20))

####Gewinn-Nachricht
def winning_message():
    SCREEN.fill(BLACK)
    winning_text = SMALL_FONT.render("Congratulations!", True, WHITE)
    text_rect = winning_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(winning_text, text_rect)
    pygame.display.flip()

#####################################################################################################################################################

#   Game-Loop 
running = True
generate_board()

##  Wait-Phase
while running:
    dt = CLOCK.tick(FPS) / 1000
    current_time = pygame.time.get_ticks()

    draw_background()
    board = draw_board()
    draw_timer()

##  Input-Phase
    # Timer aktivieren
    if first_guess and second_guess:
        if reveal_timer == 0:
            reveal_timer = current_time

    # Karten ausblenden nach 5 sek
        if current_time - reveal_timer > 2000:
            if check_guesses(first_guess_number, second_guess_number):
                matches += 1
            first_guess = False
            second_guess = False
            first_guess_number = 0
            second_guess_number = 0
            reveal_timer = 0  

    # Auf Game_over überprüfen
    if matches == ROWS * COLS // 2:
        pygame.time.delay(500)
        minigame_win += 1
        winning_message()
        pygame.time.delay(2000)
        running = False

    # Pygame quitten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Auswahl des Kärtchens 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_over:
                mouse_x, mouse_y = event.pos

                col = (mouse_x - 5) // piece_width  
                row = (mouse_y - 80) // piece_height  

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ANGEPASST
#####################################################################################################################################################
                if 0 <= col < COLS and 0 <= row < ROWS:
                    idx = col + row * COLS

                    if not first_guess:
                        first_guess, first_guess_number = True, idx

                    elif not second_guess and idx != first_guess_number and correct_matrix[row][col] == 0:
                        second_guess, second_guess_number = True, idx

# Dieser Abschnitt wurde von ChatGpt modifiziert, da ich Probleme bei der Auswahl der Karten in der ersten Row hatte, diese konnten nämlcih nicht
# immer korrekt "aufgedeckt" werden. Jetzt wird getestet, ob die ausgewählte Position auch wirklich im Spielfeld liegt und dort eine Karte ist. 
# Sonst werden nur die zwei Karten verglichen und gecheckt, ob soe ein Paar sind. SOllte das der Fall sein, wird das in der correct_matrix als 1 
# anstelle von 0 abgespeichert.
#####################################################################################################################################################

##  Double-Buffering
    pygame.display.flip()
    CLOCK.tick(FPS)

#   Pygame schließen
pygame.quit()
