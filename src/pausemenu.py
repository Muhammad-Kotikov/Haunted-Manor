# Vorbereitung
## Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren
import pygame  

from game import *  
from settings import *  
from tools import * 

### Klasse PauseMenu
class PauseMenu:
    #### Initialisierung der Klasse
    def __init__(self, text = [], sprites = []):
        #   Screen-Objekt besorgen, um aufm Bildschirm zeichnen zu können
        self.screen = pygame.display.get_surface()

        #   Schriftart festlegen 
        self.font   = pygame.font.Font('rsc/fonts/SpecialElite-Regular.ttf', 30)
        
        #   Spielspezifische Variablen
        self.text       = text          # Text der im Menü angezeigt wird
        self.sprites    = sprites       # Liste von Sprites die im Pausemenu verwendet werden
        self.running    = True          
        self.phase      = 0             # Statusphase für das Menü

    ####Render-Methode
    def render(self):
        #   Bildschirm schwarz färben
        self.screen.fill((0, 0, 0))

        #   Wenn die aktuelle Phase kleiner als die Anzahl der Sprites ist, das entsprechende Sprite zentriert anzeigen
        if self.phase < len(self.sprites):
            self.screen.blit(self.sprites[self.phase], (Resolution.WIDTH // 2 - self.sprites[self.phase].get_width() // 2, 50))

        #   Den Text Zeile für jede Zeile anzeigen
        for i, line in enumerate(self.text.split('\n')):
            #   Den Text auf dem Bildschirm an der berechneten Position anzeigen
            label = self.font.render(line, False, (255, 255, 255))
            self.screen.blit(label, (Resolution.WIDTH // 2 - label.get_width() // 2 , 250 + i * (label.get_height() + 2)))

    ####Update-Methode
    def update(self):
        for event in pygame.event.get():
            #   Fenster schließen ermöglichen
            if event.type == pygame.QUIT:
                self.running = False 
            
            #   ESC-Taste schließt das PAusenmenü
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.pausemenu = False  
            
            #   SPACE-Taste brint einen zurück ins Game(siehe Game.py)
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                pass