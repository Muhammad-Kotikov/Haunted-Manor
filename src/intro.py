#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame 
import os           #Notwendig für Dateienoperation

from game import *  
from settings import *  
from tools import * 

##### DISCLAIMER: WIR HABEN EIN INTRO ERSTELLT UND DIESES IN 111 FRAMES UNTERTEILT, DA WIR KEIN WEITERES MODUL NUTZEN SOLLTEN,DIES
##### IST NATÜRLICH NICHT DIE EFFIZENTESTE UND BESTE LÖSUNG, WENN MAN "NORMAL" EIN SPIEL DESIGNEN WÜRDE

### Klasse Intro
class Intro:
    ####Initialisierung der Klasse
    def __init__(self):
        #   Pfad zu den 111 Bildern des Intros -> nur os als Modul benutzen, kein anderes, um ein Video abzuspielen
        self.frames_path    = "rsc/sprites/videos/intro"
        
        #   Funktion get_sprite (siehe Tools) Lädt alle Frames des Videos
        self.frames         = [get_sprite(f"/videos/intro/video_frame{i:05}.png") for i in range(1,112)]
        
        #  Spielspezifische Variablen
        self.exit           = False     # Indikator, ob das Intro beendet werden soll
        self.index          = 0         # Aktueller Index der 111 Frames
        self.counter        = 0         # Counter, um Frames in regelmäßigen Abständen zu wechseln

    ####Render-Methode
    def render(self):
        #   Bildschirm schwarz 
        self.screen.fill((0, 0, 0))
        
        #   Aktuellen Frame auf Grundlage des Indexes auswählen
        frame   = self.frames[self.index]

        #   Größe und Position des Frames berechnen
        frame_rect      = frame.get_rect()
        frame_width     = frame_rect.width
        frame_height    = frame_rect.height

        #   Position in der Bildschirmmitte berechnen
        x_offset = (Resolution.WIDTH - frame_width) // 2
        y_offset = (Resolution.HEIGHT - frame_height) // 2

        #   Frame in der Bildschirmmitte anzeigen
        self.screen.blit(frame, (x_offset, y_offset))

    ####Update-Methode
    def update(self):
        #   Der Counter bekommt +1 und der Modulo berechnet die übrig gebliebene Zahl. Dadurch wird alle 4 "ticks" weitergeschaltet
        self.counter = (self.counter + 1) % 4
        
        #   Zudem erhöhtt sich dann auch der Index um 1, um den nächsten Frame anzuzeigen
        if self.counter == 0: 
            self.index += 1

        #   Wenn der letzte Frame gezeigt wurde, soll das Intro beendet werden 
        if self.index == len(self.frames) - 1:
            self.exit = True