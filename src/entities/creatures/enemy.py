from entities.creature import Creature
from entities.creature import CommandDirection
from pygame import Vector2
from settings import FRAMERATE



class Enemy(Creature):
    MAX_SPEED = 0.5                                                                                                        #Maxspeed aus Creature wird mit diesem Wert überschrieben
    ACCELERATION = MAX_SPEED / 10   
    DECELERATION = MAX_SPEED / 6
    FOLLOW_RANGE = 70                                                                                                      # Legt die Sichtweite des Gegners fest
    STOP_RANGE  = 6                                                                                                        # Wenn der Gegner in der Range ist hält er an
    radius = 10                                                                                                            # Bestimmt den Radius in dem der Gegner Schaden macht
    cooldown = FRAMERATE * 2                                                                                               # Setzt die Berechnung zur Abklinkzeit vom Gegner
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.move_towards = CommandDirection(self)                                                                         #Zieht sich die Klasse
        self.old_position = self.position.copy()                                                                           # Speichert den Startpunkt des Gegners in einer Variable
        self.path = []                                                                                                     # Sollte eigentlich den Pfad des Gegners in einer Liste speichern, damit dieser genau den weg wieder zurückläuft den er zurückgelegt hat
        self.cooldown_timer = 0                                                                                            #Abklinkzeit vom Angriff
        
    def update(self,dt):
        if not self.world.player:               
            return
        dx = self.rect.centerx-self.world.player.rect.centerx                                                              #Differenz der X Koordinate
        dy = self.rect.centery-self.world.player.rect.centery                                                              # Differenz der Y Koordinate
        if self.cooldown_timer > 0 :                                                                                       #wenn der Cooldown über 0 ist wird die if ausgeführt
            self.cooldown_timer -= 1                                                                                       #Logik unterstützt durch ChatGPT / Setzt den Cooldown um 1 runter
            self.cooldown_timer= max(0,self.cooldown_timer)                                                                #Stellt sicher das der Cooldown nicht unter 0 geht
           
        if Vector2(dx,dy).length()<self.radius :                                                                           #prüft ob sich ein Spieler im Radius befindet
            if self.cooldown_timer <= 0:                                                                                   #prüft ob der Cooldown 0 damit ein Angriff ausgeführt werden kann
                self.world.player.hit(1)                                                                                   #führt angriff auf den Spieler aus
                self.cooldown_timer = self.cooldown                                                                        #Setzt den Cooldown hoch nach dem Angriff
            

      #  self.path.append(self.position.copy())                                                                            #sollte eine Funktion werden, dass der Gegner sich seinen gelaufenen Weg merkt
        
        super().update(dt)                                                                                                 #Aktualisiert den aktuellen Zustand
    def render(self, screen, camera):                                                                                      #Rendert das Objekt auf dem Bildschirm
       
        super().render(screen, camera)

    def copy(self, x, y):
       
       return Enemy(self.hitpoints, self.sprite, x, y, self.rect.width, self.rect.height)       #

    
    def control(self):                                                                                                      #Hier wird das Verhalten des Enemys festgelegt
        
        if not self.world.player:                                                                                           #Wenn kein Spieler in der Welt gibt wird das folgende garnicht erst ausgeführt
            return
        
        #distance_x = self.world.player.position.x - self.position.x
        #distance_y = self.world.player.position.y - self.position.y                                                        # War zuerst die Logik wurde aber durch Muha`s Lösung ausgetauscht wurde unterstützt von https://www.makeuseof.com/pygame-move-enemies-different-ways/
        #distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        way = self.world.player.position - self.position                                                                    # berechnet den Vektor des Gegners zum Spieler             
        direction = Vector2(0,0)                                                                                            # Setzt den Vektor auf 0,0
        distance_to_player= way.length()                                                                                    #Berechnet aus dem Vektor die Entfernung vom Gegner zum Spieler (Muha einfach eine Maschine)
        way_to_old =  self.old_position - self.position                                                                     #Nimmt den Gespeicherten Anfangswert und berechnet den weg zum aktuellen 
        if distance_to_player < self.FOLLOW_RANGE and distance_to_player > self.STOP_RANGE and self.cooldown_timer<=0:      #Wenn die Entfernung zum Spieler im Sichtbereich des Gegners ist und außerhalb der Stop range und der Cooldown = 0 ist fängt der Gegner an den Spieler zu verfolgen
            direction = way.normalize()                                                                                      #Verringert den Abstand zum Spieler
        elif distance_to_player < self.STOP_RANGE or way_to_old.length()<0.5:                                               # Wenn der Spieler sich innerhalb der Stop Range befindet oder der Weg zum Startpunkt geringer als 0.5 ist Stoppt der Gegner. Den Wert 0.5 Haben wir gesetzt weil der Gegner sonst auf einer Stelle gezittert hat.
            direction = Vector2(0,0)                                                                                        #Stoppt den Gegner und setzt den Gegner den Vector 0,0
        else:
            direction = way_to_old.normalize()                                                                              #Wenn nichts davon zutrifft geht der Gegner zu seinem Ursprung zurück
        
        self.move_towards.execute(direction)                                                                                #Führt die Bewegung aus 
        
