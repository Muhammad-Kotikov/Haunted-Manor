# Vorbereitung
## Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren
import pygame

from settings import *
from tools import *

### Klasse Menu               
class Menu(): 
### Initialisierung der Klasse
    def __init__(self):
        #   Farben
        self.WHITE   = (255, 255, 255)
        self.BLACK   = (0, 0, 0)
        self.RED     = (120, 0, 0)

        #   Funktion zum Laden von Schriftarten
        def load_font(size):
            return pygame.font.Font(get_full_path('fonts/SpecialElite-Regular.ttf'), size)

        #   Schriftarten
        self.title_font  = load_font(120)
        self.font        = load_font(45)
        self.small_font  = load_font(20)
        
        #   Hintergrundbild laden
        self.background_image = pygame.image.load('rsc/sprites/gamemenu/gamemenu_background.png')

        #   Spezifische Variablen 
        self.start  = False
        self.exit   = False

        self.main_menu       = True
        self.credits_menu    = False
        self.options_menu    = False

        image_size = 200

        #   Checken, ob die Buttons gedrückt wurden 
        self.clicked        = False 
        self.last_clicked   = False

        #   Buttons für das Hauptmenü definieren
        self.buttons = [
            {"text": "Start Game",  "rect": pygame.Rect(50, 300, 300, 70), "clicked": False},
            {"text": "Options",     "rect": pygame.Rect(50, 400, 300, 70), "clicked": False},
            {"text": "Credits",     "rect": pygame.Rect(50, 500, 300, 70), "clicked": False},
            {"text": "Exit",        "rect": pygame.Rect(50, 600, 300, 70), "clicked": False},
        ]

        #   Toggle-Schalter für die Optionen definieren 
        self.toggle_switches = [
            {"text": "Show Debugging", "rect": pygame.Rect(50, 200, 300, 70), "state": options['debugging'], 'var': 'debugging'},    
            {"text": "Show Collison Range", "rect": pygame.Rect(50, 300, 300, 70), "state": options['collision_range'], 'var': 'collision_range'},
            {"text": "Show Movement Vectors", "rect": pygame.Rect(50, 400, 300, 70), "state": options['movement_vectors'], 'var': 'movement_vectors'},
            {"text": "Show CRT Shader", "rect": pygame.Rect(50, 500, 300, 70), "state": options['crt'], 'var': 'crt'},
            {"text": "Show Light System", "rect": pygame.Rect(50, 600, 300, 70), "state": options['lightsystem'], 'var': 'lightsystem'},
        ]

        #   Bilder für unser Team in Credits laden
        self.credits_images = [
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_sidney.png'), (image_size, image_size)), "name": "Sidney-Mae Brauer"},
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_muha.png'), (image_size, image_size)), "name": "Muhammad Kotikov"},
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_lia.png'), (image_size, image_size)), "name": "Celia Meißner"},
            {"image": pygame.transform.scale(pygame.image.load('rsc/sprites/credits_team/credits_pascal.png'), (image_size, image_size)), "name": "Pascal Simon"},
        ]

        #   Bild für den "Zurück"-Button laden 
        self.back_button_image   = pygame.image.load('rsc/sprites/gamemenu/gamemenu_backbutton.png')
        self.back_button_image   = pygame.transform.scale(self.back_button_image, (75, 75))
        self.back_button_rect    = self.back_button_image.get_rect(topleft=(20, 20))

### Update-Methode 
    def update(self):
        #   Mausposition abrufen (get_mp() siehe unten)
        self.mouse_x, self.mouse_y = get_mouse_pos()

        #   Klickzustand checken, um Menüs zu switchen oder Buttons zu tooglen 
        self.last_clicked   = self.clicked
        self.clicked        = False

        #   Fenster schließen ermöglichen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True

            #    Wenn Mousebutton gedrückt und zwar der linke, dann wird self.clicked true 
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True

                    #   Wenn wir im Hauptmenü sind, dann können wir in die anderen Menüs wechseln
                    if self.main_menu:
                        for button in self.buttons:
                            #   Überprüfen, welcher Button geklickt wurde und dann in den entsprechende state wechseln
                            if button["rect"].collidepoint(self.mouse_x, self.mouse_y):
                                button["clicked"] = True
                                if button["text"] == self.buttons[0]['text']:
                                    self.main_menu = False
                                    self.start = True
                                elif button["text"] == self.buttons[1]['text']:
                                    self.main_menu = False
                                    self.options_menu = True
                                elif button["text"] == self.buttons[2]['text']:
                                    self.main_menu = False
                                    self.credits_menu = True
                                elif button["text"] == self.buttons[3]['text']:
                                    self.exit = True
                    #   Wenn wir in einem Untermenü sind, wechseln wir beim drücken des Zurückbuttons wieder in das Hauptmenü
                    elif self.credits_menu or self.options_menu:
                        #   Überprüfen,ob der Zurückbutton gedrückt wurde 
                        if self.back_button_rect.collidepoint(self.mouse_x, self.mouse_y):
                            self.credits_menu = False
                            self.options_menu = False
                            self.main_menu = True

                            #   Dann alle Button wieder auf Nicht-Geklickt setzen, damit sie nicht mehr rot erscheinen, das war vorher ein Problem
                            for button in self.buttons:
                                button["clicked"] = False

### Render-Methode
    def render(self):
        #   Bildschirm schwarz füllen
        self.screen.fill((0, 0, 0))

        #   Je nachdem in welchem Menü wird sind, soll dieses gezeichnet werden (Funktionen siehe unten )
        if self.main_menu:
            self.screen.blit(self.background_image, (0, 0))
            self.draw_menu()
        elif self.credits_menu:
            self.draw_credits()
        elif self.options_menu:
            self.draw_options()

### Hauptmenü-Methode
    def draw_menu(self):
        #   Titel des Spiels als "Schatten" zeichnen. Dies muss zuerst geschenen, damit hier dann die weiße schrift rauf kann
        title_shadow        = self.title_font.render("Haunted Manor", True, self.BLACK)
        title_shadow_rect   = title_shadow.get_rect(center=(Resolution.WIDTH // 2 + 5, 150 + 5))
        self.screen.blit(title_shadow, title_shadow_rect)

        #   Titel des Spiels zeichnen
        title_text      = self.title_font.render("Haunted Manor", True, self.WHITE)
        title_text_rect = title_text.get_rect(center=(Resolution.WIDTH // 2, 150))
        self.screen.blit(title_text, title_text_rect)

        #   Alle Buttons im Hauptmenü werden gezeichnet
        for button in self.buttons:
            #   Wenn sie angeklickt werden, sollen sie rot hinterlegt werden . SOnst haben sie keine farbe
            if button["clicked"]:
                color = self.RED
            elif button["rect"].collidepoint(self.mouse_x, self.mouse_y):
                color = self.RED
            else:
                color = None

            if color is not None:
                pygame.draw.rect(self.screen, color, button["rect"], border_radius=10)
            
            #   Texte der vers. Auswahlmöglichkeiten werden angezeigt und auf dem Screen dargestellt
            text_surf = self.font.render(button["text"], True, self.WHITE)
            text_rect = text_surf.get_rect(topleft=(button["rect"].x + 10, button["rect"].y + (button["rect"].height - text_surf.get_height()) // 2 + 4))
            self.screen.blit(text_surf, text_rect)

### Zurückbutton-Methode 
    def draw_backbtn(self):
        #   Wenn der Button angeklickt wird, ist er rot, sonst nicht hinterlegt
        if self.back_button_rect.collidepoint(self.mouse_x, self.mouse_y):
            color = self.RED
        else:
            color = None

        if color is not None:
            pygame.draw.rect(self.screen, color, self.back_button_rect.inflate(10, 10), border_radius=15)
        self.screen.blit(self.back_button_image, self.back_button_rect)

### Credits-Menu-Methode
    def draw_credits(self):
            self.screen.fill(self.BLACK)
            self.draw_backbtn()

            #   Bilder sollen 200 px mit 50 px Spacing sein
            image_size  = 200
            spacing     = 50
            start_x = (Resolution.WIDTH - 4 * image_size - 3 * spacing) // 2

            #   Es wird durch die Bilder mit Namen furch iteriert
            for idx, developer in enumerate(self.credits_images):
                x = start_x + idx * (image_size + spacing)
                y = Resolution.HEIGHT // 2 - image_size // 2

                image_rect = developer["image"].get_rect(center=(x + image_size // 2, y + image_size // 2 - 20))
                self.screen.blit(developer["image"], image_rect)

                name_text = self.small_font.render(developer["name"], True, self.WHITE)
                name_rect = name_text.get_rect(center=(x + image_size // 2, y + image_size))
                self.screen.blit(name_text, name_rect)

### Options-Menü-Methode
    def draw_options(self):
        last_click_time = 0
        self.screen.fill(self.BLACK)
        self.draw_backbtn()

        #   Cool-down wird benötigt, damit die Toogle switches 
        current_time    = pygame.time.Clock() 
        click_cooldown  = 0.1

        #   Toggle-Schalter für Optionen zeichnen
        for toggle_switch in self.toggle_switches:
            #   Status der Toggle-Schalter definieren
            if toggle_switch["state"]:
                state_text = "ON"  
                color = (0, 255, 0) 
            else:
                state_text = "OFF"  
                color = (255, 0, 0)  

            #   Text für die Beschreibung des Schalters anzeigen
            text_surf = self.font.render(f"{toggle_switch['text']}", True, self.WHITE)
            text_rect = text_surf.get_rect(topleft=(toggle_switch["rect"].x, toggle_switch["rect"].y))
            self.screen.blit(text_surf, text_rect)

            #   Text für den Schalter selbst anzeigen 
            state_text_surf = self.font.render(state_text, True, color)
            state_text_rect = state_text_surf.get_rect(topleft=(toggle_switch["rect"].x + 1000, toggle_switch["rect"].y))
            self.screen.blit(state_text_surf, state_text_rect)

            #   Toggle-Schalter Zustand ändern wenn auf den Text geklickt wird und die Wartezeit um ist
            #   Var wird in den Settings umgeschaltet mit der Funktion toggle
            if pygame.mouse.get_pressed()[0] and state_text_rect.collidepoint(self.mouse_x, self.mouse_y) and self.clicked and not self.last_clicked:
                toggle_switch["state"] = not toggle_switch["state"]
                toggle(toggle_switch['var'])
