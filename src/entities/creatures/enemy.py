import pygame
import copy
from settings import *
from collider import *
from entities.creature import Creature
from entities.creatures.player import *
import random
import abc




enemies= []

class enemyState(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod

    def alive(self):
        pass

    def dead(self):
        pass
    
    def damage(self):
        pass


    def patrol(self):
        pass


    
    def stand(self):
        pass

    def follow(self):
        pass

    def attack(self):
        pass


    pass


class enemyAlive(enemyState):
    pass

class enemyDead(enemyState):
    pass
class enemyPatrol(enemyState):
   
    pass

class enemyStand(enemyState):
    pass

class ememyfollow(enemyState):
    pass
class enemyAttack(enemyState):
    
    pass
class Enemy(Creature,):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.health = 3
        self.moving = False
        
        #enemies.append(self)
        #self.zustandsuebergang(enemyState(self))
   

        pass
    

    def enemy_alive(self):
        #wenn Health >0  ist dann enemy alive
        if self.health > 0:
            self.enemy_alive = True
        pass

    def enemy_dead(self):
        #Wenn Health = 0 ist dann enemy dead true
        if self.health == 0:
            self.enemyDead= True
        pass
    
    def enemy_moving(self):
        if self.moving==True:
            self.speed= 2
       #direction = random.choice(['left', 'right', 'up', 'down'])
        #Gegner bewegt sich zufällig VON EINER WEBSITE QUELLE NICHT VERGESSEN!!!!!!
        #if direction == 'left':
         #   self.position.x -= 1
        #elif direction == 'right':
         #   self.position.x += 1
        #elif direction == 'up':
         #   self.position.y -= 1
        #elif direction == 'down':
         #   self.position.y += 1
        # Calculate the distance between the enemy and the player
        #https://www.makeuseof.com/pygame-move-enemies-different-ways/
     
        

        pass
    
    
    def enemy_nomoving(self):
        if self.moving== False:
            self.speed= 0
        #Gegner bewegt sich nicht und steht still
        pass
    
    
    def enemy_chasing(self):
        #https://www.makeuseof.com/pygame-move-enemies-different-ways/
        distance_x = self.world.player.position.x- self.position.x
        distance_y = self.world.player.position.y - self.position.y
        self.distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

        if self.distance < 22  :
            enemyStand

        else :
            speed = 2

        if self.distance <80:
            if self.distance != 2:
                self.position.x += speed * distance_x / self.distance
                self.position.y += speed * distance_y / self.distance
        pass
    
    
    def enemy_attacking(self):
        #Wenn der der Gegner eine gewisse Entfernung unterschreitet führt dieser den Befehl attack aus
        if self.distance < 22 :
            self.speed = 0
            pass



    def update(self,dt):
        self.enemy_moving()
        self.enemy_chasing()
        super().update(dt)

    pass














#class Enemy:
 #   def __init__(self, x, y):
  #      self.x = x
   #     self.y = y

#enemy = Enemy(100, 100)  # Beispiel-Startposition






# Move the enemy randomly on the screen
#direction = random.choice(['left', 'right', 'up', 'down'])

#if direction == 'left':
 #   enemy.x -= 5
#elif direction == 'right':
 #   enemy.x += 5
#elif direction == 'up':
 #   enemy.y -= 5
#elif direction == 'down':
 #   enemy.y += 5


#class Enemy(Creature):

 #   def __init__(self,  *args, **kwargs):
  #      super().__init__(*args, **kwargs)
   #     self.health = 3
    #    enemies.append(self)
       
    
        
    #def update(self, player_center):
    # Berechne die Richtung vom Gegner zum Spieler
        #enemy_center = pygame.Vector2(self.position)
       # player_center = pygame.Vector2(player_center)
       # direction = player_center - enemy_center

    # Normalisieren der Richtung und Geschwindigkeit berechnen
        #if direction.length() > 0:
            #direction = direction.normalize()
        #self.velocity = direction * self.speed

    # Position aktualisieren
       #self.position += self.velocity

        
        
        
        

     #   player_center = Player.get_center()
      #  enemy_center = self.get_center()

       # self.velocity = [player_center[0] - enemy_center[0], player_center[1] - enemy_center[1]]

        #magnitude = (self.velocity[0]**2+self.velocity[1]**2) **0.5
        #self.velocity = [self.velocity[0] / magnitude * self.speed, self.velocity[1] / magnitude * self.speed]