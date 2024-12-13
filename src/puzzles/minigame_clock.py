#   Mithilfe von: https://www.youtube.com/watch?v=bmLuz8ISn20 erstellt
#   Quelle Bild: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flume.de%2Fde%2Fgrossuhr-ersatzteile%2Fzifferblaetter-zubehoer%2Fzifferblaetter%2Froemische-zahlen%2Fzifferblatt-aluminium-roemische-zahlen-oe-178-mm%2F334966&psig=AOvVaw09Nzh0TlKbj4LI5cwo9fmX&ust=1731253425590000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLibot7Lz4kDFQAAAAAdAAAAABAE
#   Das Bild wurde eigenständig an die Bedürfnisse angepasst

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame
import sys
import math
import time

### Screen-Einstellungen
WIDTH   = 800
HEIGHT  = 800
SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN + pygame.SCALED)
FPS     = 60

### Pygame initialisieren
pygame.init()
pygame.display.set_caption("Clock")

### Farben
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)

### Schriftarten
FONT            = pygame.font.Font(None, 100)
SMALL_FONT      = pygame.font.Font(None, 100)

### Hintergrundbild 
background_image = pygame.image.load('rsc/sprites/minigame_clock_image.png')

##  Spielspezifische Vorbereitung
### Uhr-Variablen
CENTER          = (WIDTH // 2, HEIGHT // 2)
C_WIDTH         = WIDTH // 2
C_HEIGHT        = HEIGHT // 2
RADIUS          = 250

### Zeiger-Positionen
hour_angle          = math.radians(360 * (1 / 12)) 
minute_angle        = math.radians(360 * (30 / 60)) 
second_angle        = math.radians(360 * (15 / 60)) 

selected_clockhand  = None
tolerance           = 0.1

### Zielzeit
target_hour         = math.radians(360 * (3 / 12))    
target_minute       = math.radians(360 * (30 / 60))   
target_second       = math.radians(360 * (15 / 60))     

### Minispiel-Gewinn
minigame_win        = 0
game_over           = False
last_correct_time   = None  

### Funktionen
####Zeichnen der Zeiger
def draw_clock(hour_angle, minute_angle, second_angle):
    # Hintergrundbild
    SCREEN.blit(background_image, (0, 0))

    # Stundenzeiger
    x_hour = C_WIDTH + RADIUS * 0.5 * math.cos(hour_angle - math.pi / 2)
    y_hour = C_HEIGHT + RADIUS * 0.5 * math.sin(hour_angle - math.pi / 2)
    pygame.draw.line(SCREEN, BLACK, CENTER, (x_hour, y_hour), 12)

    # Minutenzeiger
    x_minute = C_WIDTH + RADIUS * 0.75 * math.cos(minute_angle - math.pi / 2)
    y_minute = C_HEIGHT + RADIUS * 0.75 * math.sin(minute_angle - math.pi / 2)
    pygame.draw.line(SCREEN, BLACK, CENTER, (x_minute, y_minute), 8)

    # Sekundenzeiger
    x_second = C_WIDTH + RADIUS * 1 * math.cos(second_angle - math.pi / 2)
    y_second = C_HEIGHT + RADIUS * 1 * math.sin(second_angle - math.pi / 2)
    pygame.draw.line(SCREEN, RED, CENTER, (x_second, y_second), 3)

    # Mittelpunkt
    pygame.draw.circle(SCREEN, BLACK, CENTER, 20) 

####Auswahl Zeiger
def chose_clockhand(clockhand_angle, radius, mouse_pos):
    # Endpunkt des Zeigers
    clockhand_x = C_WIDTH + radius * math.cos(clockhand_angle - math.pi / 2)
    clockhand_y = C_HEIGHT + radius * math.sin(clockhand_angle - math.pi / 2)

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ANGEPASST
#####################################################################################################################################################
    # Abstand von der Maus zur Zeigerlinie
    num_points = 20  
    for i in range(num_points + 1):
        # Position jedes Punkts entlang des Zeigers
        current_x = C_WIDTH + (radius * i / num_points) * math.cos(clockhand_angle - math.pi / 2)
        current_y = C_HEIGHT + (radius * i / num_points) * math.sin(clockhand_angle - math.pi / 2)
        
        # Abstand von Punkt zu Maus berechnen
        distance = math.sqrt((mouse_pos[0] - current_x)**2 + (mouse_pos[1] - current_y)**2)
        
        # Wenn der Abstand zu einem Punkt entlang des Zeigers klein genug ist, haben wir einen Treffer
        if distance < 20:  
            return True
    
    return False

# ChatGpt hat hier geholfen, dass das Greifen bzw. Erkennen des Mauszeigers an dem Uhrenzeiger besser gelingt. Zuvor konnte man den Zeiger nur am
# Ende greifen, nun kann man ihn überall greifen und dann draggen. Es wird also für jeden Abschnitt der Abstand zur Maus berechnet und wenn die
# Maus weniger als 20px entfernt ist, kann der Zeiger gegriffen werden
#####################################################################################################################################################

####Gewinn-Nachricht
def winning_message():
    SCREEN.fill(BLACK)
    winning_text = SMALL_FONT.render("Congratulations!", True, WHITE)
    text_rect = winning_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(winning_text, text_rect)
    pygame.display.flip()

####Uhrzeit checken
def check_time(hour_angle, minute_angle, second_angle):
    if (target_hour - tolerance < hour_angle < target_hour + tolerance) and \
       (target_minute - tolerance < minute_angle < target_minute + tolerance) and \
       (target_second - tolerance < second_angle < target_second + tolerance):
        return True
    return False

#####################################################################################################################################################

# Game-Loop
running = True

##  Wait-Phase
while running:
    current_time = pygame.time.get_ticks()

##  Input-Phase
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                mouse_x, mouse_y = pygame.mouse.get_pos()

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ANGEPASST
#####################################################################################################################################################   
                if chose_clockhand(hour_angle, RADIUS * 0.5, (mouse_x, mouse_y)):
                    selected_clockhand = 'hour'
                    # Startwinkel
                    offset_hour = math.atan2(mouse_y - CENTER[1], mouse_x - CENTER[0]) - hour_angle
                
                elif chose_clockhand(minute_angle, RADIUS * 0.75, (mouse_x, mouse_y)):
                    selected_clockhand = 'minute'
                    # Startwinkel
                    offset_minute = math.atan2(mouse_y - CENTER[1], mouse_x - CENTER[0]) - minute_angle

                elif chose_clockhand(second_angle, RADIUS * 1, (mouse_x, mouse_y)):
                    selected_clockhand = 'second'
                    # Startwinkel
                    offset_second = math.atan2(mouse_y - CENTER[1], mouse_x - CENTER[0]) - second_angle

        if event.type == pygame.MOUSEBUTTONUP:
            if selected_clockhand:
                selected_clockhand = None 

        if event.type == pygame.MOUSEMOTION and selected_clockhand:
            mouse_x, mouse_y = event.pos

            angle = math.atan2(mouse_y - CENTER[1], mouse_x - CENTER[0])

            if selected_clockhand == 'hour':
                hour_angle = angle - offset_hour

            elif selected_clockhand == 'minute':
                minute_angle = angle - offset_minute

            elif selected_clockhand == 'second':
                second_angle = angle - offset_second

    draw_clock(hour_angle, minute_angle, second_angle)  

# Dieser Abschnitt wurde mithilfe von Chatgpt angepasst, um das Verschieben des Mauszeigers nahtlos zu ermöglichen und nicht leicht "stoppend". Das 
# das Spielerlebnis besser und angenehmer. Hier wird die Mausposition verfolgt.
#####################################################################################################################################################

    # Überprüfen ob die Zeit korrekt ist
    if check_time(hour_angle, minute_angle, second_angle):
        if not game_over:  
            game_over = True 
            winning_time = time.time()

    if game_over and time.time() - winning_time >= 3:
        minigame_win += 1
        winning_message()
        pygame.time.delay(2000)
        running = False

## Double-Buffering
    pygame.display.flip()

# Pygame schließen
pygame.quit()
sys.exit()
