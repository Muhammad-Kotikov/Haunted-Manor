from entities.creature import Creature
from entities.creature import CommandDirection
from pygame import Vector2



class Enemy(Creature):
    MAX_SPEED = 1.2
    ACCELERATION = MAX_SPEED / 5
    DECELERATION = MAX_SPEED / 6
    FOLLOW_RANGE = 100
    STOP_RANGE  = 6
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmd = CommandDirection(self)
        self.old_position = self.position.copy()
        self.path = []
        
    def update(self,dt):

        if self.world.player and self.rect.colliderect(self.world.player.rect) == True:
            self.world.player.hit(1)

      #  self.path.append(self.position.copy())
        
        super().update(dt)
    def render(self, screen, camera):
       
        super().render(screen, camera)

    def copy(self, x, y):
       
       return Enemy(self.hitpoints, self.sprite, x, y, self.rect.width, self.rect.height)

    
    def control(self):
        
        if not self.world.player:
            return
        
        #distance_x = self.world.player.position.x - self.position.x
        #distance_y = self.world.player.position.y - self.position.y
        #distance = (distance_x ** 2 + distance_y ** 2) ** 0.5
        way = self.world.player.position - self.position
        direction = Vector2(0,0)
        distance_to_player= way.length()
        way_to_old =  self.old_position - self.position

        if distance_to_player < self.FOLLOW_RANGE and distance_to_player > self.STOP_RANGE:
            direction = way.normalize()
        elif distance_to_player < self.STOP_RANGE or way_to_old.length()<0.5:
            direction = Vector2(0,0)
        else:
            direction = way_to_old.normalize()
        
        self.cmd.execute(direction)
        
