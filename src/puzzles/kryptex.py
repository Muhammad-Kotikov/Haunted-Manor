#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame 

### Screen-Einstellungen
WIDTH       = 1000
HEIGHT      = 800
SCREEN      = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN + pygame.SCALED)
FPS         = 60      

### Pygame initialisieren
pygame.init()
pygame.display.set_caption("Kryptex")

####        Wie kann ich ein Pygame-Fenster in einem bereits vorhandenen Fenster öffnen?

### Clock-Objekt
CLOCK       = pygame.time.Clock()

### Farben
WHITE       = (255, 255, 255)
BLACK       = (0, 0, 0)
GRAY        = (150, 150, 150)  

### Schriftarten
FONT        = pygame.font.Font(None, 200)
SMALL_FONT  = pygame.font.Font(None, 100)

##  Spielspezifische Vorbereitung
target_word         = "HAUNTED"

letter_width        = FONT.size("A")[0]
kryptex_text        = ["A"] * len(target_word)
spacing             = 20

minigame_win        = 0
game_over           = False


### Position Buchstaben
x                   = WIDTH // 2 - (len(target_word) // 2 * letter_width + len(target_word) // 2 * spacing)
y                   = HEIGHT // 2

letters             = []

for letter in kryptex_text:
    letters.append({
        "char"  : letter,
        "index" : 0,
        "pos"   : (x, y)
    })
    x += letter_width + spacing

### Funktionen
####Gewinn-Nachricht
def winning_message():
    SCREEN.fill(BLACK)
    winning_text    = SMALL_FONT.render("Congratulations!", True, WHITE)
    text_rect       = winning_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(winning_text, text_rect)
    pygame.display.flip()

####Buchstaben anzeigen
def draw_letters(selected_letter):
    for p, letter in enumerate(letters):
        color           = GRAY if selected_letter == p else WHITE
        letter_surface  = FONT.render(letter["char"], True, color)
        letter_rect     = letter_surface.get_rect(center=letter["pos"])
        SCREEN.blit(letter_surface, letter_rect)

#####################################################################################################################################################

#   Game-Loop
running                 = True
selected_letter         = None

##  Wait-Phase
while running:
    dt = CLOCK.tick(FPS) / 1000
    current_time = pygame.time.get_ticks()

##  Input-Phase
    for event in pygame.event.get():
        # Pygame quitten
        if event.type == pygame.QUIT:
            running = False             

    # Buchstaben auswählen
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            for p, letter in enumerate(letters):
                letter_surface = FONT.render(letter["char"], True, GRAY if selected_letter == p else WHITE)
                letter_rect = letter_surface.get_rect(center=letter["pos"])

                if letter_rect.collidepoint(mouse_pos):  
                    selected_letter = p if selected_letter != p else None  
                    break

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ERSTELLT
#####################################################################################################################################################
        # Buchstaben von A bis Z oder andersherum "drehen"                                                                                                #
        elif not game_over and event.type == pygame.MOUSEWHEEL and selected_letter is not None:                                                     #         
            letters[selected_letter]["index"] = (letters[selected_letter]["index"] + event.y) % 26                                                  #
            letters[selected_letter]["char"] = chr(letters[selected_letter]["index"] + ord('A'))                                                    #
                                                                                                                                                    #
            # Überprüfung der Zeichenkette ermöglichen                                                                                                        #
            current_text = ''.join([letter["char"] for letter in letters])                                                                          #
                                                                                                                                                    #
# ChatGpt wurde hier verwendet, um das "Drehen" der Buchstaben zu ermöglichen, damit sie in der richtigen Reihenfolge sowohl von A nach Z als auch  #
# von Z nach A durchgehbar und darstellbar. Dies hätte auch mithilfe von einer Liste erreicht werden können, wäre aber wesentlich umständlicher und #
# unschöner. Zudem musste ich einen Weg finden, um die Buchstaben effektiv und kompakter abgleichen zu können, dies geschieht mit der ord()-Funktion#
#####################################################################################################################################################

            # Zeichenkette überprüfen -> Spiel gewonnen ?
            if current_text == target_word:                                                                                                       
                time = current_time     
                displayed_time = pygame.time.get_ticks()                                                                                                 
                game_over = True

##  Render-Phase
    # Buchstaben auf Bildschirm anzeigen
    SCREEN.fill(BLACK)
    if not game_over:
        draw_letters(selected_letter)

    elif game_over and current_time - displayed_time < 1500:
        draw_letters(selected_letter)

    else:
        minigame_win += 1
        winning_message()
        pygame.time.delay(2000)
        running = False

##  Double-Buffering
    pygame.display.flip()

#   Pygame schließen (nicht mehr notwendig)
#pygame.quit()
