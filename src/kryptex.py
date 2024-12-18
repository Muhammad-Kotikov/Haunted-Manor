# Vorbereitung
## Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren
import pygame 

from settings import Resolution, FRAMERATE
from tools import *

### Klasse Kryptex
class Kryptex():                 
### Initialisierung der Klasse
    def __init__(self): 
        #   Farben
        self.WHITE       = (255, 255, 255)      
        self.BLACK       = (0, 0, 0)           
        self.RED         = (120, 0, 0) 

        # Schriftarten 
        self.FONT        = pygame.font.Font(None, 200)
        self.SMALL_FONT  = pygame.font.Font(None, 100)
        
        #   Spielspezifische Variablen     
        self.TARGET_WORD = "CKRAUSS"                # Zielwort          
        self.SPACING     = 20                       # Abstand zwischen den Buchstaben 

        self.won                 = False            
        self.won_timer           = FRAMERATE * 1    # Timer für den Gewinn
        self.congrats_timer      = FRAMERATE * 3    # Timer für die Glückwunschnachricht
        self.exit                = False            

        self.mouse_pos           = (0, 0)           # Mausposition
        self.letters             = []               # Leere Liste für die Buchstaben
        self.selected_letter = None                 

        #   Breite eines Buchstabens berechenen
        letter_width        = self.FONT.size("A")[0]

        #   Positionen für die einzelne Buchstaben berehcnen 
        x                   = Resolution.WIDTH // 2 - (len(self.TARGET_WORD) // 2 * letter_width + len(self.TARGET_WORD) // 2 * self.SPACING)
        y                   = Resolution.HEIGHT // 2

        #   Für jeden Buchstaben im Zielwort wird Anfangs ein A angezeigt. Diese kann man dann von A bis Z rotieren 
        for letter in ["A"] * len(self.TARGET_WORD):
            self.letters.append({
                "char"  : letter,               # Buchstabe
                "index" : 0,                    # Index des Buchstabens
                "pos"   : (x, y)                # Position des Buchstabens
            })
            x += letter_width + self.SPACING    # Neue x-Position aufgrund des Spacings berechnen

### Update-Methode                   
    def update(self):
        #   Wenn das Spiel gewonnen wurde + der Timer noch läuft
        if self.won and self.won_timer > 0:
            self.won_timer -= 1
            self.selected_letter = None
            return
        
        #   Wenn der Timer für den Gewinn abgelaufen ist, startet der Timer für die Glückwunsch-Nachricht
        elif self.won_timer <= 0 and self.congrats_timer > 0:
            self.congrats_timer -= 1
            return
        
        #   Wenn der Glückwunsch-Timer abgelaufen ist, wird das Spiel beendet 
        elif self.congrats_timer <= 0:
            self.exit = True
            return
        
        if self.won == False:
            self.exit = False

        #   Aktuelle Mausposition holen (siehe def get_mp, weiter unten)
        self.mouse_pos = get_mp(self)

        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit = True
                self.lost = True

            #   Auf Mausdrücken überprüfen 
            elif event.type == pygame.MOUSEBUTTONDOWN:

                #   Auf Anklicken eines Buchstabens prüfen 
                for p, letter in enumerate(self.letters):
                    #   Wenn der Buchstabe angeklickt/ oder drübergehovert wird, soll er sich Grau färben
                    letter_surface = self.FONT.render(letter["char"], True, self.RED if self.selected_letter == p else self.WHITE)
                    letter_rect = letter_surface.get_rect(center=letter["pos"])
                    if letter_rect.collidepoint(self.mouse_pos): 
                        self.selected_letter = p if self.selected_letter != p else None
                        break

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ERSTELLT
###############################################################################################################################################################
            #   Auf Mausraddrehen überprüfen
            elif event.type == pygame.MOUSEWHEEL and self.selected_letter is not None:  
                #   Die Buchstaben werden durch "iteriert"
                self.letters[self.selected_letter]["index"] = (self.letters[self.selected_letter]["index"] + event.y) % 26
                self.letters[self.selected_letter]["char"] = chr(self.letters[self.selected_letter]["index"] + ord('A'))  # Setze den Buchstaben
                                                                                                                           
# ChatGpt wurde hier verwendet, um das "Drehen" der Buchstaben zu ermöglichen, damit sie in der richtigen Reihenfolge sowohl von A nach Z als auch  #
# von Z nach A durchgehbar und darstellbar. Dies hätte auch mithilfe von einer Liste erreicht werden können, wäre aber wesentlich umständlicher und #
# unschöner. Zudem musste ich einen Weg finden, um die Buchstaben effektiv und kompakter abgleichen zu können, dies geschieht mit der ord()-Funktion#
#####################################################################################################################################################
                
                #   Überprüfung der Zeichenkette ermöglichen                                                                                                        
                current_text = ''.join([letter["char"] for letter in self.letters])

                #   Wenn das Zielwort richtig ist, bricht das Spiel ab
                if current_text == self.TARGET_WORD: 
                    self.won = True  

### Render-Methode
    def render(self):
        #   Hintergrund schwarz färben
        self.screen.fill(self.BLACK) 

        #   Wenn das Spiel gewonnen wurde und der Timer abgelaufen ist, wird die Gewinnnachricht angezeigt (siehe unten)
        if self.won and self.won_timer <= 0:
            self.draw_winning_message() 
            return
        #   Wenn das Spiel beendet werden soll(siehe Game.py)
        elif self.exit: 
            return
        #   Wenn noch nichts passiert ist, werden die Buchstaben dargestellt 
        else:
            self.draw_letters() 

### Draw-Letters-Methode
    def draw_letters(self):
        #   Für jeden Biuchstaben wird die Farbe bestimmt und dann wird die POberfläche für den Buchstaben erstellt und dessen Position berechnet
        for p, letter in enumerate(self.letters):
            # Bestimme die Farbe des Buchstabens (rot, wenn er ausgewählt wurde)
            color           = self.RED if self.selected_letter == p else self.WHITE
            letter_surface  = self.FONT.render(letter["char"], True, color) 
            letter_rect     = letter_surface.get_rect(center=letter["pos"])  
            self.screen.blit(letter_surface, letter_rect)  

### Winning-Message-Methode
    def draw_winning_message(self):
        winning_text    = self.SMALL_FONT.render("Congratulations!", True, self.WHITE)
        text_rect       = winning_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(winning_text, text_rect)