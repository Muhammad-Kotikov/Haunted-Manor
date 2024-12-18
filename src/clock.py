#   Mithilfe von: https://www.youtube.com/watch?v=bmLuz8ISn20 erstellt
#   Quelle Bild: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flume.de%2Fde%2Fgrossuhr-ersatzteile%2Fzifferblaetter-zubehoer%2Fzifferblaetter%2Froemische-zahlen%2Fzifferblatt-aluminium-roemische-zahlen-oe-178-mm%2F334966&psig=AOvVaw09Nzh0TlKbj4LI5cwo9fmX&ust=1731253425590000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLibot7Lz4kDFQAAAAAdAAAAABAE
#   Das Bild wurde eigenständig an die Bedürfnisse angepasst

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame  
import math  

from settings import Resolution, FRAMERATE  
from tools import *  

### Klasse Clock
class Clock():
### Klasse initialisieren
    def __init__(self):
        #   Farben definieren
        self.WHITE  = (255, 255, 255)
        self.BLACK  = (0, 0, 0)
        self.RED     = (255, 0, 0)

        #   Mittelpunkt der Uhr bestimmen
        self.CENTER     = (Resolution.WIDTH // 2, Resolution.HEIGHT // 2)
        self.C_WIDTH    = Resolution.WIDTH // 2  
        self.C_HEIGHT   = Resolution.HEIGHT // 2 
        self.RADIUS     = 250       # Ausprobieren, damit es mit dem Bild passt 

        #   Zielwinkel der Zeiger 
        self.TARGET_HOUR    = math.radians(360 * (11 / 12))  # Zielstunde: 11 Uhr
        self.TARGET_MINUTE  = math.radians(360 * (33 / 60))  # Zielminute: 33 Minuten
        self.TARGET_SECOND  = math.radians(360 * (45 / 60))  # Zielsekunde: 45 Sekunden

        #   Toleranzbereich für das Ziel
        self.ANGLE_TOLERANCE = 0.1

        #   Startwinkel der Zeiger
        self.angle_hour     = math.radians(360 * (2 / 12)) 
        self.angle_minute   = math.radians(360 * (30 / 60))  
        self.angle_second   = math.radians(360 * (15 / 60))  

        #   Spielspezifische Variablen
        self.FONT = pygame.font.Font('rsc/fonts/SpecialElite-Regular.ttf', 80) 
        self.BACKGROUND_IMAGE = get_sprite('minigame_clock_image.png')  
        self.selected_clockhand = None 

        #    Spielspezifische Variablen
        self.won            = False    
        self.exit           = False 
        self.mouse_pos      = (0, 0) 
        self.offset_hour    = 0  
        self.offset_minute  = 0  
        self.offset_second  = 0  

### Update-Methode
    def update(self):
        #   Gewonnen-Status überprüfen


        #   Prüfen, ob die Zielzeit erreicht wurde
        if self.check_time():  
            self.won = True

        if self.won:
            self.exit = True
            return

        #   Ereignisse prüfen 
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit = True
                self.lost = True

            #   Linksklick prüfen
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
                mouse_x, mouse_y = get_mouse_pos()  
                #   Stundenzeiger auswählen
                if self.chose_clockhand(self.angle_hour, self.RADIUS * 0.5, (mouse_x, mouse_y)):
                    self.selected_clockhand = 'hour'
                    self.offset_hour = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0]) - self.angle_hour
                #   Minutenzeiger auswählen
                elif self.chose_clockhand(self.angle_minute, self.RADIUS * 0.75, (mouse_x, mouse_y)):
                    self.selected_clockhand = 'minute'
                    self.offset_minute = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0]) - self.angle_minute
                #   Sekundenzeiger auswählen
                elif self.chose_clockhand(self.angle_second, self.RADIUS * 1, (mouse_x, mouse_y)):
                    self.selected_clockhand = 'second'
                    self.offset_second = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0]) - self.angle_second

            #   Maustaste loslassen
            elif event.type == pygame.MOUSEBUTTONUP:  
                self.selected_clockhand = None 

            #   Mausbewegung bei ausgewähltem Zeiger
            elif event.type == pygame.MOUSEMOTION and self.selected_clockhand:  
                mouse_x, mouse_y = get_mouse_pos()
                angle = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0])
                if self.selected_clockhand == 'hour':
                    self.angle_hour = self.normalize_angle(angle - self.offset_hour)
                elif self.selected_clockhand == 'minute':
                    self.angle_minute = self.normalize_angle(angle - self.offset_minute)
                elif self.selected_clockhand == 'second':
                    self.angle_second = self.normalize_angle(angle - self.offset_second)
        
### Zeichnen der Uhr
    def render(self):
        #   Hintergrund schwarz färben
        if self.won:
            return

        #   Hintergrundbild der Uhr zeichnen
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        #   Stundenzeiger zeichnen
        x_hour = self.C_WIDTH + self.RADIUS * 0.5 * math.cos(self.angle_hour - math.pi / 2)
        y_hour = self.C_HEIGHT + self.RADIUS * 0.5 * math.sin(self.angle_hour - math.pi / 2)
        pygame.draw.line(self.screen, self.BLACK, self.CENTER, (x_hour, y_hour), 12)

        #   Minutenzeiger zeichnen
        x_minute = self.C_WIDTH + self.RADIUS * 0.75 * math.cos(self.angle_minute - math.pi / 2)
        y_minute = self.C_HEIGHT + self.RADIUS * 0.75 * math.sin(self.angle_minute - math.pi / 2)
        pygame.draw.line(self.screen, self.BLACK, self.CENTER, (x_minute, y_minute), 8)

        #   Sekundenzeiger zeichnen
        x_second = self.C_WIDTH + self.RADIUS * 1 * math.cos(self.angle_second - math.pi / 2)
        y_second = self.C_HEIGHT + self.RADIUS * 1 * math.sin(self.angle_second - math.pi / 2)
        pygame.draw.line(self.screen, self.RED, self.CENTER, (x_second, y_second), 3)

        #   Mittelpunkt der Uhr zeichnen
        pygame.draw.circle(self.screen, self.BLACK, self.CENTER, 20)


### CHATGPT GENERATED METHOD
    def normalize_angle(self, angle):
        while angle < 0:
            angle += 2 * math.pi
        while angle >= 2 * math.pi:
            angle -= 2 * math.pi
        return angle

### Prüfen, ob die Zielzeit erreicht wurde
    def check_time(self):
        
        if ((self.TARGET_HOUR - self.ANGLE_TOLERANCE < self.angle_hour < self.TARGET_HOUR + self.ANGLE_TOLERANCE)) and \
           (self.TARGET_MINUTE - self.ANGLE_TOLERANCE < self.angle_minute < self.TARGET_MINUTE + self.ANGLE_TOLERANCE) and \
           (self.TARGET_SECOND - self.ANGLE_TOLERANCE < self.angle_second < self.TARGET_SECOND + self.ANGLE_TOLERANCE):
            return True
        return False
    

#                                           DER FOLGENDE ABSCHNITT WURDE DURCH *CHATGPT* ANGEPASST
#####################################################################################################################################################
### Auswahl des Uhrenzeigers     
    def chose_clockhand(self, clockhand_angle, radius, mouse_pos):
        #   Abstand von der Maus zur Zeigerlinie
        num_points = 20  
        for i in range(num_points + 1):
            #   Position jedes Punkts entlang des Zeigers
            current_x = self.C_WIDTH + (radius * i / num_points) * math.cos(clockhand_angle - math.pi / 2)
            current_y = self.C_HEIGHT + (radius * i / num_points) * math.sin(clockhand_angle - math.pi / 2)
            
            #   Abstand von Punkt zu Maus berechnen
            distance = math.sqrt((mouse_pos[0] - current_x)**2 + (mouse_pos[1] - current_y)**2)
            
            #   Wenn der Abstand zu einem Punkt entlang des Zeigers klein genug ist, haben wir einen Treffer
            if distance < 20:  
                return True
        
        return False
    
# ChatGpt hat hier geholfen, dass das Greifen bzw. Erkennen des Mauszeigers an dem Uhrenzeiger besser gelingt. Zuvor konnte man den Zeiger nur am
# Ende greifen, nun kann man ihn überall greifen und dann draggen. Es wird also für jeden Abschnitt der Abstand zur Maus berechnet und wenn die
# Maus weniger als 20px entfernt ist, kann der Zeiger gegriffen werden
#####################################################################################################################################################