import pygame
from settings import TILE_SIZE
from abc import abstractmethod

from entity import Entity
from collider import * 

vec = pygame.math.Vector2

from patterns import Command

class CommandDirection(Command):

    def execute(self, direction : vec):
        self.receiver.target_direction = direction

class Creature(Entity):

    INVUNERABLE_FRAMES = 60

    MAX_SPEED = 1.5
    ACCELERATION = MAX_SPEED / 6
    DECELERATION = MAX_SPEED / 4

    COLLISION_DETECTION_RANGE = 2

    IDLE = 0
    RUNNING = 1
    STOPPING = 2


    def __init__(self, hitpoints : int = 1, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.velocity = vec(0, 0)
        self.target_direction = vec(0,0)
        
        self.collider = SimpleCollider()

        # hitpoints = maximale Lebenspunkte, health = momentane Lebenspunkte (z.B. nach dem man verletzt wurde)
        self.hitpoints = hitpoints
        self.health = hitpoints

        self.invunerable = False
        self.i_frames_left = 0

        self.acc_fac = 1
        self.spd_fac = 1

    @abstractmethod
    def control(self):
        pass

    def update(self, dt):
        super().update()

        self.delta_time = dt

        # get player intent
        self.control()

        # move, collide and slide the character
        self.move_and_slide()

        if self.invunerable:
            self.i_frames_left -= 1

        if self.i_frames_left <= 0:
            self.invunerable = False
            self.untint()


    def render(self, screen, camera):
        super().render(screen, camera)

    def hit(self, damage):

        if self.invunerable:
            return

        self.health -= damage

        if self.health <= 0:
            self.die()
            return

        self.invunerable = True
        self.i_frames_left = self.INVUNERABLE_FRAMES
        self.tint((255, 255, 255, 80), pygame.BLEND_RGB_ADD)
    
    def move(self):


        # https://www.youtube.com/watch?v=YJB1QnEmlTs (An In-Depth look at Lerp, Smoothstep, and Shaping Functions)
        def smoothstep(t : float):
            v1 = t ** 2
            v2 = 1.0 - (1.0 - t) ** 2
            return pygame.math.lerp(v1, v2, t)
        

        if self.target_direction != vec(0, 0):
            self.movement_state = self.RUNNING
            new_speed = min((self.velocity.length() + self.ACCELERATION * self.acc_fac * self.delta_time), self.MAX_SPEED * self.spd_fac)
            direction = self.target_direction
        

        elif self.target_direction == vec(0, 0) and self.velocity.length() > 0:
            self.movement_state = self.STOPPING
            new_speed = max((self.velocity.length() - self.DECELERATION * self.acc_fac * self.delta_time), 0)
            direction = self.velocity.normalize()


        else:
            self.movement_state = self.IDLE
            new_speed = 0
            direction = vec(0, 0)


        """ uncomment when player ignores max speed, math.lerp "soft clamps" it anyway so not really needed """
        if self.velocity.length() > 0:
            self.velocity.clamp_magnitude_ip(self.MAX_SPEED * self.spd_fac)
        

        self.velocity = pygame.math.lerp(0, self.MAX_SPEED * self.spd_fac, smoothstep(new_speed / (self.MAX_SPEED * self.spd_fac))) * direction


      

    def slide(self):

        
        # Spielerkoordinate in tiles, (aus der Mitte des Charakters) zu berechnen
        creature_tile_x = round(self.rect.centerx / TILE_SIZE)
        creature_tile_y = round(self.rect.centery / TILE_SIZE)

        # Der Koordinateninvervall in der nach Kollision gecheckt werden soll
        collision_range_x = (pygame.math.clamp(creature_tile_x - self.COLLISION_DETECTION_RANGE, 0, self.world.width - 1), pygame.math.clamp(creature_tile_x + self.COLLISION_DETECTION_RANGE, 0, self.world.width - 1))
        collision_range_y = (pygame.math.clamp(creature_tile_y - self.COLLISION_DETECTION_RANGE, 0, self.world.height - 1), pygame.math.clamp(creature_tile_y + self.COLLISION_DETECTION_RANGE, 0,  self.world.height - 1))

        collision_objects = []

        # "*tuple" unpacks the values inside the tuple and uses them as paremeters for a function
        for tile_y in range(*collision_range_y):
            for tile_x in range(*collision_range_x):
                if self.world.tile_map[tile_y][tile_x] != None and self.world.tile_map[tile_y][tile_x].has_collision == True:
                    collision_objects.append(self.world.tile_map[tile_y][tile_x])
        
        for interactable in self.world.interactables:
            if interactable.has_collision:
                collision_objects.append(interactable)

        self.position += self.velocity

        self.collider.collide_with_wall(self, collision_objects)

    def move_and_slide(self):

        # calculate velocity (without collision) based on player intent
        self.move()

        # check collision and slide character along walls
        self.slide()
        

    def die(self):
        self.world.unregister_creature(self)


    def copy(self, x, y):
        return Creature(self.hitpoints, self.sprite, x, y, self.rect.width, self.rect.height)