from entities.creature import Creature
from entities.creature import CommandDirection
from pygame import Vector2
from settings import FRAMERATE
from tools import *


#Setzt Standardwerte der Klasse Enemy
class Enemy(Creature):
    MAX_SPEED = 0.8                                                                                                        #Maxspeed aus Creature wird mit diesem Wert überschrieben
    ACCELERATION = MAX_SPEED / 10                                                                                          #Beschleunigungsrate
    DECELERATION = MAX_SPEED / 6                                                                                           #Verzögerungsrate
    FOLLOW_RANGE = 80                                                                                                      # Bereich in dem der Gegner den Spieler folgt
    STOP_RANGE  = 6                                                                                                       #Bereich in dem der Gegner zum Spieler stoppt ansonsten buggt er in den Spieler
    radius = 10                                                                                                            #Radius für den Angriff
    cooldown = FRAMERATE * 2                                                                                               #Abklinkzeit vom Angriff
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_towards = CommandDirection(self)                                                                         #Kommando um sich in eine Richtung zu bewegen
        self.old_position = self.position.__copy__()                                                                       # ChatGPT hat mir gezeigt wie ich den Anfangspunkt Kopieren kann und speichern kann/Speichert den Startpunkt des Gegners in einer Variable
        self.path = []                                                                                                     # Sollte eigentlich den Pfad des Gegners in einer Liste speichern, damit dieser genau den weg wieder zurückläuft den er zurückgelegt hat
        self.cooldown_timer = 0                                                                                            #Abklinkzeit vom Angriff
        
    def update(self,dt):
        if not self.world.player:                                                                                          #Wenn kein Spieler existiert, passiert nichts
            return
        dx = self.rect.centerx-self.world.player.rect.centerx                                                              #Differenz der X Koordinate; Die X und Y Werte haben wir genommen, damit die Mitte vom Spieler & Gegner genommen wird
        dy = self.rect.centery-self.world.player.rect.centery                                                              # gleiche für Y Koordinate
        if self.cooldown_timer > 0 :                                                                                        #Cooldown damit der Gegner nicht endlos Schaden zufügt
            self.cooldown_timer -= 1                                                                                       #Logik unterstützt durch ChatGPT / Setzt den Cooldown um 1 runter solange der Cooldown über 0 ist
            self.cooldown_timer= max(0,self.cooldown_timer)                                                                #Stellt sicher das der Cooldown nicht unter 0 fällt
           
        if Vector2(dx,dy).length() < self.radius :                                                                           #prüft ob sich ein Spieler im Radius befindet
            if self.cooldown_timer <= 0:                                                                                   #prüft ob der Cooldown 0 damit ein Angriff ausgeführt werden kann
                self.world.player.hit(1)                                                                                   #führt angriff auf den Spieler aus
                self.cooldown_timer = self.cooldown                                                                        #Setzt den Cooldown hoch nach dem Angriff
            

      #  self.path.append(self.position.copy())                                                                            #sollte eine Funktion werden, dass der Gegner sich seinen gelaufenen Weg merkt
        
        super().update(dt)                                                                                                
    def render(self, screen, camera):                                                                                      #Rendert den Gegner
       
        super().render(screen, camera)

    def copy(self, x, y):                                                                                                  #Kopiert den Gegner an eine neue Stelle
       
       return Enemy(self.hitpoints, self.sprite, x, y, self.rect.width, self.rect.height)       

    
    def control(self):                                                                                                      #Hier wird das Verhalten des Enemys festgelegt
        
        if not self.world.player:                                                                                           
            return
                                                                                                                            #Gegner Verhalten unterstützt von: https://www.makeuseof.com/pygame-move-enemies-different-ways/                                                           
        way = self.world.player.position - self.position                                                                         
        direction = Vector2(0,0)                                                                                            #Standard Richtung (Keine Bewegung)
        distance_to_player= way.length()                                                                                    
        way_to_old =  self.old_position - self.position                                                                     
        if distance_to_player < self.FOLLOW_RANGE and distance_to_player > self.STOP_RANGE and self.cooldown_timer<=0:      
            direction = way                                                                                                 #Gegner bewegt sich zum Spieler hier reicht der Wert "way", da die Berechnung in Commanddirection passiert
        elif distance_to_player < self.STOP_RANGE or way_to_old.length()<0.5:                                               # Wenn der Spieler sich innerhalb der Stop Range befindet oder der Weg zum Startpunkt geringer als 0.5 ist Stoppt der Gegner. Den Wert 0.5 Haben wir gesetzt weil der Gegner sonst auf einer Stelle gezittert hat.
            direction = Vector2(0,0)                                                                                        
        else:
            direction = way_to_old                                                                                           #Wenn nichts davon zutrifft geht der Gegner zu seinem Ursprung zurück
        
        self.move_towards.execute(direction)                                                                                
        
