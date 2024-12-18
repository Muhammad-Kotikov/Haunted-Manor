#   Mithilfe von: https://www.youtube.com/watch?v=IzsX89ZYGT0&t=625s erstellt

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import random
import pygame

from settings import Resolution, FRAMERATE
from tools import get_mp

### Klasse Memory
class Memory():
    #### Initialisierung der Klasse
    def __init__(self):
        #   Farben
        self.WHITE       = (255, 255, 255)
        self.BLACK       = (0, 0, 0)
        self.GRAY        = (128, 128, 128)
        self.RED         = (255, 0, 0)

        #   Anzahl der Reihen und Spalten des Spielfelds (Achtung muss immer eine gerade summe sein)
        self.ROWS        = 6
        self.COLS        = 6
        try: 
            self.ROWS * self.COLS % 2 == 0
        except:
            print("Ungerade Anzahl an Karten")
    
        #   Breite und Höhe der einzelnen Pieces bestimmen
        self.PIECE_WIDTH     = Resolution.WIDTH // self.COLS
        self.PIECE_HEIGHT    = (Resolution.HEIGHT - 75) // self.ROWS

        #   Schriftarten
        self.FONT        = pygame.font.Font(None, 100)
        self.SMALL_FONT  = pygame.font.Font(None, 75)

        #   Spielspezifische Variablen 
        self.won                 = False
        self.won_timer           = FRAMERATE * 1  # Timer nach  Sieg
        self.congrats_timer      = FRAMERATE * 3  # Timer für Gewinn-Bildschirm

        self.lost                = False
        self.lost_timer          = FRAMERATE * 3  # Timer nach Niederlage

        self.exit                = False        

        #   Es wird eine Matrix, um alle korrekte Matches zu speichern
        #   0 bedeutet, Karte nicht gefunden, 1 bedeutet die Karten sind aufgedeckt und 2 bedeutet die Karten sind ein Match gewesen 
        self.correct_matrix  = [[0] * self.COLS for _ in range(self.ROWS)]

        #   Variablen für Spieleraktionen
        self.first_guess     = False  
        self.second_guess    = False  

        #   Indexe der Karten werden gespeichert 
        self.first_guess_number  = 0
        self.second_guess_number = 0

        self.matches         = 0    
        self.reveal_timer    = 0    
        self.start_time      = pygame.time.get_ticks()  
        self.spaces_list     = []  

### Update-Methode
    def update(self):
        #   Timer nach einem Sieg oder einer Niederlage
        if self.won and self.won_timer > 0:
            self.won_timer -= 1
            return  
        #   Wenn der Timer abgelaufen ist reduziert sich der Gewinn Timer um die NAchricht anzuzeigen
        elif self.won_timer <= 0 and self.congrats_timer > 0:
            self.congrats_timer -= 1
            return  
        #   Wenn auch der Timer abgelaufen ist, wird das Spiel beendet
        elif self.congrats_timer <= 0:
            self.exit = True  
            return
        #   Wenn das Spiel verloren wurde reduziert sich der Lost-Timer
        elif self.lost and self.lost_timer > 0:
            self.lost_timer -= 1
            return  
        #   Wenn der Lost-Timer abgelaufen ist, wird das Spiel beendet
        elif self.lost_timer <= 0:
            self.exit = True  
            return

        #   Wenn zwei Karten ausgewählt wurden, startet ein Timer, bis die Karten wieder umgedreht werden 
        if self.first_guess and self.second_guess:
            self.reveal_timer += 1 

        #   Hier werden die Karten dann wieder umgedreht 
        if self.reveal_timer > FRAMERATE * 0.75:  
            #   Hier wird geprüft ob die Karten übereinstimmen
            if self.check_guesses(self.first_guess_number, self.second_guess_number):
                self.matches += 1 
            #   Die Kartenauswahl wird zurückgesetzt
            self.first_guess    = False
            self.second_guess   = False
            self.first_guess_number     = 0
            self.second_guess_number    = 0
            self.reveal_timer   = 0 

        #   Hier wird überprüft, ob alle Paare gefunden wurden, dafür können wir die Ganzzahldivision nehmen
        if self.matches == self.ROWS * self.COLS // 2:
            self.won = True 

        if self.won == False:
            self.exit = False
        for event in pygame.event.get():
            #    Wenn Mousebutton gedrückt, wird die Position mithilfe von mp_get() geholt  
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit = True
                self.lost = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = get_mp(self)
                #   Dann wird sowohl die Spalte als auch die Zeile basierend auf der Position gesucht 
                col = (mouse_x - 5) // self.PIECE_WIDTH
                row = (mouse_y - 80) // self.PIECE_HEIGHT  

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ANGEPASST
#####################################################################################################################################################
                if 0 <= col < self.COLS and 0 <= row < self.ROWS:
                    idx = col + row * self.COLS 
                    
                    #   Erster Kartenversuch: Setzt die erste Auswahl
                    if not self.first_guess:
                        self.first_guess, self.first_guess_number = True, idx
                    #   Zweiter Kartenversuch: Setzt die zweite Auswahl
                    #   Es  wird überprüft, dass die zweite Karte nicht dieselbe wie die erste ist und noch nicht korrekt ist
                    elif not self.second_guess and idx != self.first_guess_number and self.correct_matrix[row][col] == 0:
                        self.second_guess, self.second_guess_number = True, idx

# Dieser Abschnitt wurde von ChatGpt modifiziert, da ich Probleme bei der Auswahl der Karten in der ersten Row hatte, diese konnten nämlcih nicht
# immer korrekt "aufgedeckt" werden. Jetzt wird getestet, ob die ausgewählte Position auch wirklich im Spielfeld liegt und dort eine Karte ist. 
# Sonst werden nur die zwei Karten verglichen und gecheckt, ob soe ein Paar sind. SOllte das der Fall sein, wird das in der correct_matrix als 1 
# anstelle von 0 abgespeichert.
#####################################################################################################################################################

### Render-Methode
    def render(self):
        #   Hintergrund schwarz füllen
        self.screen.fill(self.BLACK)  
            #   Verschiedene Zustände anzeigen
        if self.won and self.won_timer <= 0:
                #   Gewinnnachricht
            self.draw_winning_message()  
            return
        elif self.lost and self.lost_timer >= 0:
                #   Verliernachricht
            self.draw_losing_message() 
            return
        elif self.exit:
            return
        else:
            self.draw_background()  
            self.draw_board()       
            self.draw_timer()       

### Enter-Methode
    def enter(self):
        self.lost = False
        #   Timer für das Aufdecken von Karten
        self.reveal_timer = 0  
        #   Spielzeit
        self.game_timer = 90 * 1000
        self.spaces_list = []
        self.generate_board()

### Zurücksetzen des Spiels 
    def reset(self):
        self.won = False
        #   Timer für die Anzeige des Gewinnbildschirms
        self.won_timer = FRAMERATE * 1
        self.congrats_timer = FRAMERATE * 3

        #   Timer für die Verlieranzeige 
        self.lost = False
        self.lost_timer = FRAMERATE * 3

        self.exit = False

        #   Matrix, die den Status der Karten
        self.correct_matrix = [[0] * self.COLS for _ in range(self.ROWS)]

        #   Initialisiere Variablen für die beiden Karten, die verglichen werden
        self.first_guess        = False
        self.second_guess       = False
        self.first_guess_number     = 0
        self.second_guess_number    = 0

        #   Anzahl der gefundenen Paare
        self.matches = 0
        #   Timer für das Aufdecken von Karten
        self.reveal_timer = 0  
        #   Starte den Spieltimer
        self.start_time = pygame.time.get_ticks()
        #   Liste der Kartenpositionen leeren
        self.spaces_list = []

### Hintergund-Methode
    def draw_background(self):
        pygame.draw.rect(self.screen, self.BLACK, [0, 0, Resolution.WIDTH, 75])
        pygame.draw.rect(self.screen, self.GRAY, [0, 75, Resolution.WIDTH, Resolution.HEIGHT])

### Karten auf dem Spielfeld anzeigen
    def generate_board(self):
        #   Liste aller möglichen Karten
        options_list = []
        #   Temporäre Liste, um genutzte Karten zu speichern
        used_pieces = []

        for item in range(self.ROWS * self.COLS // 2):
            options_list.append(item)

        #   Spielfeld zufällig mit Karten befüllen
        for item in range(self.ROWS * self.COLS):
            piece = options_list[random.randint(0, (len(options_list)-1))]
            self.spaces_list.append(piece)

            #   Paare löschen, sobald beide Karten verwendet wurden
            if piece in used_pieces:
                used_pieces.remove(piece)
                options_list.remove(piece)
            else:
                used_pieces.append(piece)

### Spielfeld-Methode
    def draw_board(self):
        for i in range(self.COLS):  
            for j in range(self.ROWS):
                x = i * self.PIECE_WIDTH 
                y = j * self.PIECE_HEIGHT 

                #   Verdeckte Karten als weiße Rechtecke zeichen
                if self.correct_matrix[j][i] == 0: 
                    piece = pygame.draw.rect(self.screen, self.WHITE, 
                                            [x + 5, y + 80, self.PIECE_WIDTH - 10, self.PIECE_HEIGHT - 10], 0, 4)

                #   Text auf die umgedrehten Kärtchen zeichen matrix == 1 ist umgedreht
                elif self.correct_matrix[j][i] == 1: 
                    piece_text = self.FONT.render(str(self.spaces_list[i + j * self.COLS]), True, self.GRAY)
                    self.screen.blit(piece_text, 
                                    (x + 5 + (self.PIECE_WIDTH - 10) // 2 - piece_text.get_width() // 2, 
                                    y + 80 + (self.PIECE_HEIGHT - 10) // 2 - piece_text.get_height() // 2))
                    
                #   Matrix == 2 ist korrekt, also entfernen 
                elif self.correct_matrix[j][i] == 2:  
                    continue 

                #   Beide Karten einmal anzeigen 
                if (self.first_guess and self.first_guess_number == i + j * self.COLS) or \
                (self.second_guess and self.second_guess_number == i + j * self.COLS):
                    piece_text = self.FONT.render(str(self.spaces_list[i + j * self.COLS]), True, self.GRAY)
                    self.screen.blit(piece_text, 
                                    (x + 5 + (self.PIECE_WIDTH - 10) // 2 - piece_text.get_width() // 2, 
                                    y + 80 + (self.PIECE_HEIGHT - 10) // 2 - piece_text.get_height() // 2))

### Paare checken-Methode
    def check_guesses(self, first, second):
        #   Wenn die Nummer der beiden KArten gleich ist, werden die beiden karten an der entsprechenden Stelle entfernt 
        if self.spaces_list[first] == self.spaces_list[second]: 
            col1, row1 = first % self.COLS, first // self.COLS  
            col2, row2 = second % self.COLS, second // self.COLS 
            self.correct_matrix[row1][col1] = self.correct_matrix[row2][col2] = 2  
            return True
        else:
            return False

### Timer-Methode
    def draw_timer(self):
        passed_time     = pygame.time.get_ticks() - self.start_time  
        remaining_time  = self.game_timer - passed_time  

        if remaining_time < 0:  
            remaining_time = 0
            self.lost = True

        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000

        #   Timer zentriert anzeigen 
        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = self.SMALL_FONT.render(timer_text, True, self.WHITE)
        self.screen.blit(timer_surface, (Resolution.WIDTH // 2 - timer_surface.get_width() // 2, 20))

### Gewinn-Methode 
    def draw_winning_message(self):
        winning_text = self.SMALL_FONT.render("Congratulations!", True, self.WHITE)
        text_rect = winning_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(winning_text, text_rect)

### Verlier-Methode
    def draw_losing_message(self):
        loosing_text = self.SMALL_FONT.render("GAME OVER!", True, self.RED)
        text_rect = loosing_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(loosing_text, text_rect)