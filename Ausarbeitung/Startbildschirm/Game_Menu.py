#   Mithilfe von:  erstellt

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame

### Screen-Einstellungen
WIDTH   = 1200
HEIGHT  = 800
SCREEN  = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
FPS     = 60

##  Pygame initialisieren
pygame.init()
pygame.display.set_caption("Haunted Manor")

##  Clock-Objekt
CLOCK   = pygame.time.Clock()

### Farben
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (120, 0, 0)

### Schriftarten
def load_font(size):
    return pygame.font.Font('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Schriftarten/SpecialElite-Regular.ttf', size)

TITLE_FONT  = load_font(120)
FONT        = load_font(45)
SMALL_FONT  = load_font(20)

### Hintergrundbild 
background_image    = pygame.image.load('//Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Grafiken/Game Menu_Image_Background.png')

### Sound 
    #### from https://freesound.org/people/klankbeeld/sounds/523330/
pygame.mixer.music.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Sound/Sound_Rain_Wind.wav')
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(.1)

##  Spezifische Vorbereitung
main_menu       = True
credits_menu    = False
options_menu    = False

### Buttons
buttons = [
    {"text": "Start Game", "rect": pygame.Rect(50, 300, 300, 70), "clicked": False},
    {"text": "Options", "rect": pygame.Rect(50, 400, 300, 70), "clicked": False},
    {"text": "Credits", "rect": pygame.Rect(50, 500, 300, 70), "clicked": False},
    {"text": "Exit", "rect": pygame.Rect(50, 600, 300, 70), "clicked": False},
]

### Bilder für Entwickler-Team
credits_images = [
    {"image": pygame.image.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Grafiken/Unknown-1.jpeg'), "name": "Sidney-Mae Brauer"},
    {"image": pygame.image.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Grafiken/Unknown-1.jpeg'), "name": "Muhammad Kotikov"},
    {"image": pygame.image.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Grafiken/Unknown-1.jpeg'), "name": "Celia Meißner"},
    {"image": pygame.image.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Grafiken/Unknown-1.jpeg'), "name": "Pascal Simon"},
]

### Bild für Back-Button
back_button_image    = pygame.image.load('/Users/sidney/Documents/Studium/WS 24_25/PROG2/Spiel /Ausarbeitung/Startbildschirm/Grafiken/Game Menu_Image_Back Button.png')
back_button_image   = pygame.transform.scale(back_button_image, (75, 75))
back_button_rect    = back_button_image.get_rect(topleft=(20, 20))

### Funktionen
####Hauptmenü darstellen
def draw_menu():
    title_text      = TITLE_FONT.render("Haunted Manor", True, WHITE)
    title_text_rect = title_text.get_rect(center=(WIDTH // 2, 150))
    SCREEN.blit(title_text, title_text_rect)

    title_shadow        = TITLE_FONT.render("Haunted Manor", True, BLACK)
    title_shadow_rect   = title_shadow.get_rect(center=(WIDTH // 2 + 5, 150 + 5))
    SCREEN.blit(title_shadow, title_shadow_rect)

    mouse_pos = pygame.mouse.get_pos()

    for button in buttons:
        if button["clicked"]:
            color = RED
        elif button["rect"].collidepoint(mouse_pos):
            color = RED
        else:
            color = None

        if color is not None:
            pygame.draw.rect(SCREEN, color, button["rect"], border_radius=10)
        text_surf = FONT.render(button["text"], True, WHITE)
        text_rect = text_surf.get_rect(topleft=(button["rect"].x + 10, button["rect"].y + (button["rect"].height - text_surf.get_height()) // 2 + 4))
        SCREEN.blit(text_surf, text_rect)

####Zurück-Button darstellen
def draw_backbtn():
    mouse_pos = pygame.mouse.get_pos()
    if back_button_rect.collidepoint(mouse_pos):
        color = RED
    else:
        color = None

    if color is not None:
        pygame.draw.rect(SCREEN, color, back_button_rect.inflate(10, 10), border_radius=15)
    SCREEN.blit(back_button_image, back_button_rect)

####Credit-Menü darstellen
def draw_credits():
    SCREEN.fill(BLACK)
    draw_backbtn()

    image_size = 200
    margin = 50
    start_x = (WIDTH - 4 * image_size - 3 * margin) // 2

    for idx, developer in enumerate(credits_images):
        x = start_x + idx * (image_size + margin)
        y = HEIGHT // 2 - image_size // 2

        image_rect = developer["image"].get_rect(center=(x + image_size // 2, y + image_size // 2 - 20))
        SCREEN.blit(developer["image"], image_rect)

        name_text = SMALL_FONT.render(developer["name"], True, WHITE)
        name_rect = name_text.get_rect(center=(x + image_size // 2, y + image_size))
        SCREEN.blit(name_text, name_rect)

####Options-Menü darstellen
def draw_options():
    SCREEN.fill(BLACK)
    draw_backbtn()

    options_text = FONT.render("Options", True, WHITE)
    options_text_rect = options_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(options_text, options_text_rect)

####Game darstellen
def draw_game():
    SCREEN.fill(WHITE)

#####################################################################################################################################################

# Game-Loop
running = True

while running:
    if main_menu:
        SCREEN.blit(background_image, (0,0))
        draw_menu()
    elif credits_menu:
        draw_credits()
    elif options_menu:
        draw_options()
    else:  # Hauptspiel startet
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        draw_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if main_menu:
                    for button in buttons:
                        if button["rect"].collidepoint(mouse_x, mouse_y):
                            button["clicked"] = True
                            if button["text"] == "Start Game":
                                main_menu = False
                            elif button["text"] == "Options":
                                main_menu = False
                                options_menu = True
                            elif button["text"] == "Credits":
                                main_menu = False
                                credits_menu = True
                            elif button["text"] == "Exit":
                                running = False
                elif credits_menu or options_menu:
                    if back_button_rect.collidepoint(mouse_x, mouse_y):
                        credits_menu = False
                        options_menu = False
                        main_menu = True

                        for button in buttons:
                            button["clicked"] = False

    pygame.display.update()
    CLOCK.tick(FPS)

pygame.quit()
