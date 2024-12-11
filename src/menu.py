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

        self.background_image = pygame.image.load(get_full_path('Game Menu_Image_Background.png'))


        pygame.mixer.music.load(get_full_path('Sound_Rain_Wind.wav'))
        pygame.mixer.music.set_volume(.1)
        pygame.mixer.music.play(-1, 0.0)
        
    
        ##  Spezifische Vorbereitung
        self.main_menu       = True
        self.credits_menu    = False
        self.options_menu    = False

        ### Buttons
        self.buttons = [
            {"text": "Start Game",  "rect": pygame.Rect(50, 300, 300, 70), "clicked": False},
            {"text": "Options",     "rect": pygame.Rect(50, 400, 300, 70), "clicked": False},
            {"text": "Credits",     "rect": pygame.Rect(50, 500, 300, 70), "clicked": False},
            {"text": "Exit",        "rect": pygame.Rect(50, 600, 300, 70), "clicked": False},
        ]

        ### Bilder für Entwickler-Team
        self.credits_images = [
            {"image": pygame.image.load(get_full_path('Unknown-1.jpeg')), "name": "Sidney-Mae Brauer"},
            {"image": pygame.image.load(get_full_path('Unknown-1.jpeg')), "name": "Muhammad Kotikov"},
            {"image": pygame.image.load(get_full_path('Unknown-1.jpeg')), "name": "Celia Meißner"},
            {"image": pygame.image.load(get_full_path('Unknown-1.jpeg')), "name": "Pascal Simon"},
        ]

        ### Bild für Back-Button
        self.back_button_image   = pygame.image.load(get_full_path('Game Menu_Image_Back Button.png'))
        self.back_button_image   = pygame.transform.scale(self.back_button_image, (75, 75))
        self.back_button_rect    = self.back_button_image.get_rect(topleft=(20, 20))


    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    if self.main_menu:
                        for button in self.buttons:
                            if button["rect"].collidepoint(mouse_x, mouse_y):
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
                        if self.back_button_rect.collidepoint(mouse_x, mouse_y):
                            self.credits_menu = False
                            self.options_menu = False
                            self.main_menu = True

                            for button in self.buttons:
                                button["clicked"] = False


    def render(self):

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
        title_text      = self.title_font.render("Haunted Manor", True, self.WHITE)
        title_text_rect = title_text.get_rect(center=(Resolution.WIDTH // 2, 150))
        self.screen.blit(title_text, title_text_rect)

        title_shadow        = self.title_font.render("Haunted Manor", True, self.BLACK)
        title_shadow_rect   = title_shadow.get_rect(center=(Resolution.WIDTH // 2 + 5, 150 + 5))
        self.screen.blit(title_shadow, title_shadow_rect)

        mouse_pos = pygame.mouse.get_pos()

        for button in self.buttons:
            if button["clicked"]:
                color = self.RED
            elif button["rect"].collidepoint(mouse_pos):
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
        mouse_pos = pygame.mouse.get_pos()
        if self.back_button_rect.collidepoint(mouse_pos):
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
        self.screen.fill(self.BLACK)
        self.draw_backbtn()

        options_text = self.font.render("Options", True, self.WHITE)
        options_text_rect = options_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(options_text, options_text_rect)

"""
    ####Game darstellen
    def draw_game(self):
        self.screen.fill(self.WHITE)
"""
