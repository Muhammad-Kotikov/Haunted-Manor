import pygame
from settings import *
from tools import *

class Menu(): 

    WHITE   = (255, 255, 255)
    BLACK   = (0, 0, 0)
    RED     = (120, 0, 0)

    def __init__(self):

        # Muha: start gibt der GameState weiter dass das eigentliche Spiel starten soll
        # Exit dass das komplette Programm beendet werden soll
        self.start = False
        self.exit = False

        def load_font(size):
            return pygame.font.Font(get_full_path('fonts/SpecialElite-Regular.ttf'), size)

        self.title_font  = load_font(120)
        self.font        = load_font(45)
        self.small_font  = load_font(20)

        self.background_image = pygame.image.load('rsc/sprites/gamemenu/gamemenu_background.png')


        pygame.mixer.music.load('rsc/sounds/gamemenu_wind_rain.wav')
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1, 0.0)
        
    
        ##  Spezifische Vorbereitung
        self.main_menu       = True
        self.credits_menu    = False
        self.options_menu    = False

        image_size = 200

        self.clicked = False
        self.last_clicked = False

        ### Buttons
        self.buttons = [
            {"text": "Start Game",  "rect": pygame.Rect(50, 300, 300, 70), "clicked": False},
            {"text": "Options",     "rect": pygame.Rect(50, 400, 300, 70), "clicked": False},
            {"text": "Credits",     "rect": pygame.Rect(50, 500, 300, 70), "clicked": False},
            {"text": "Exit",        "rect": pygame.Rect(50, 600, 300, 70), "clicked": False},
        ]

        self.toggle_switches = [
            {"text": "Show Debugging", "rect": pygame.Rect(50, 300, 300, 70), "state": options['debugging'], 'var': 'debugging'},    
            {"text": "Show Collison Range", "rect": pygame.Rect(50, 400, 300, 70), "state": options['collision_range'], 'var': 'collision_range'},
            {"text": "Show Movement Vectors", "rect": pygame.Rect(50, 500, 300, 70), "state": options['movement_vectors'], 'var': 'movement_vectors'},
        ]

        ### Bilder fürs Team
        self.credits_images = [
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_sidney.png'), (image_size, image_size)), "name": "Sidney-Mae Brauer"},
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_muha.png'), (image_size, image_size)), "name": "Muhammad Kotikov"},
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_lia.png'), (image_size, image_size)), "name": "Celia Meißner"},
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_pascal.png'), (image_size, image_size)), "name": "Pascal Simon"},
        ]

        ### Bild für Back-Button
        self.back_button_image   = pygame.image.load('rsc/sprites/gamemenu/gamemenu_backbutton.png')
        self.back_button_image   = pygame.transform.scale(self.back_button_image, (75, 75))
        self.back_button_rect    = self.back_button_image.get_rect(topleft=(20, 20))

    def update(self):

        self.mouse_x, self.mouse_y = self.get_mp()

        self.last_clicked = self.clicked
        self.clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                    if self.main_menu:
                        for button in self.buttons:
                            if button["rect"].collidepoint(self.mouse_x, self.mouse_y):
                                button["clicked"] = True
                                if button["text"] == "Start Game":
                                    self.main_menu = False
                                    self.start = True
                                elif button["text"] == "Options":
                                    self.main_menu = False
                                    self.options_menu = True
                                elif button["text"] == "Credits":
                                    self.main_menu = False
                                    self.credits_menu = True
                                elif button["text"] == "Exit":
                                    self.exit = True
                    elif self.credits_menu or self.options_menu:
                        if self.back_button_rect.collidepoint(self.mouse_x, self.mouse_y):
                            self.credits_menu = False
                            self.options_menu = False
                            self.main_menu = True

                            for button in self.buttons:
                                button["clicked"] = False

    def render(self):

        self.screen.fill((0, 0, 0))

        if self.main_menu:
            self.screen.blit(self.background_image, (0, 0))
            self.draw_menu()
        elif self.credits_menu:
            self.draw_credits()
        elif self.options_menu:
            self.draw_options()
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()


    def draw_menu(self):
        title_shadow        = self.title_font.render("Haunted Manor", True, self.BLACK)
        title_shadow_rect   = title_shadow.get_rect(center=(Resolution.WIDTH // 2 + 5, 150 + 5))
        self.screen.blit(title_shadow, title_shadow_rect)

        title_text      = self.title_font.render("Haunted Manor", True, self.WHITE)
        title_text_rect = title_text.get_rect(center=(Resolution.WIDTH // 2, 150))
        self.screen.blit(title_text, title_text_rect)

        for button in self.buttons:
            if button["clicked"]:
                color = self.RED
            elif button["rect"].collidepoint(self.mouse_x, self.mouse_y):
                color = self.RED
            else:
                color = None

            if color is not None:
                pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            text_surf = self.font.render(button["text"], True, self.WHITE)
            text_rect = text_surf.get_rect(topleft=(button["rect"].x + 10, button["rect"].y + (button["rect"].height - text_surf.get_height()) // 2 + 4))
            self.screen.blit(text_surf, text_rect)

    ####Zurück-Button darstellen
    def draw_backbtn(self):
        if self.back_button_rect.collidepoint(self.mouse_x, self.mouse_y):
            color = self.RED
        else:
            color = None

        if color is not None:
            pygame.draw.rect(self.screen, color, self.back_button_rect.inflate(10, 10), border_radius=15)
        self.screen.blit(self.back_button_image, self.back_button_rect)

    ####Credit-Menü darstellen
    def draw_credits(self):
        self.screen.fill(self.BLACK)
        self.draw_backbtn()

        image_size = 200
        margin = 50
        start_x = (Resolution.WIDTH - 4 * image_size - 3 * margin) // 2

        for idx, developer in enumerate(self.credits_images):
            x = start_x + idx * (image_size + margin)
            y = Resolution.HEIGHT // 2 - image_size // 2

            image_rect = developer["image"].get_rect(center=(x + image_size // 2, y + image_size // 2 - 20))
            self.screen.blit(developer["image"], image_rect)

            name_text = self.small_font.render(developer["name"], True, self.WHITE)
            name_rect = name_text.get_rect(center=(x + image_size // 2, y + image_size))
            self.screen.blit(name_text, name_rect)

    ####Options-Menü darstellen
    def draw_options(self):
        last_click_time = 0
        self.screen.fill(self.BLACK)
        self.draw_backbtn()

        current_time = pygame.time.Clock() 
        click_cooldown = 0.1  # Längerer Cooldown von 1 Sekunde

        for toggle_switch in self.toggle_switches:
            # Definieren des Status Textes
            if toggle_switch["state"]:
                state_text = "ON"  
                color = (0, 255, 0)  # Grün für ON
            else:
                state_text = "OFF"  
                color = (255, 0, 0)  # Rot für OFF

            # Text für den Schalter (z.B. "Show Debugging")
            text_surf = self.font.render(f"{toggle_switch['text']}", True, self.WHITE)
            text_rect = text_surf.get_rect(topleft=(toggle_switch["rect"].x, toggle_switch["rect"].y))
            self.screen.blit(text_surf, text_rect)

            # Text für den ON/OFF Status (grün oder rot)
            state_text_surf = self.font.render(state_text, True, color)
            state_text_rect = state_text_surf.get_rect(topleft=(toggle_switch["rect"].x + 1000, toggle_switch["rect"].y))
            self.screen.blit(state_text_surf, state_text_rect)

            # Toggle-Switch Zustand ändern, wenn auf den Status Text geklickt wird und die Wartezeit um ist
            if pygame.mouse.get_pressed()[0] and state_text_rect.collidepoint(self.mouse_x, self.mouse_y) and self.clicked and not self.last_clicked:
                # Schalte den Zustand der Option um
                toggle_switch["state"] = not toggle_switch["state"]
                toggle(toggle_switch['var'])

                # Debugging-Meldung für die Zustände der Optionen
                print(f"Option '{toggle_switch['text']}' is now {'ON' if toggle_switch['state'] else 'OFF'}")

    def get_mp(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int(mouse_x / Resolution.SCALE - Resolution.X_OFFSET)
        mouse_y = int(mouse_y / Resolution.SCALE - Resolution.Y_OFFSET)

        return mouse_x, mouse_y

"""
    ####Game darstellen
    def draw_game(self):
        self.screen.fill(self.WHITE)
"""
