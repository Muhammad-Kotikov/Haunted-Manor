import pygame
import copy
from settings import *
from collider import Collider
from entity.creature.creature import Creature

MAX_SPEED = 3
ACCELERATION = MAX_SPEED / 6
DECELERATION = MAX_SPEED / 4
TURN_SPEED = DECELERATION

# Keymapping
LEFT = pygame.K_a
RIGHT = pygame.K_d
UP = pygame.K_w
DOWN = pygame.K_s

# Movement states
STOPPED = 0
ACCELERATING = 1
DECELERATING = 2


COLLISION_DETECTION_RANGE = 2

vec = pygame.Vector2

class Player(Creature):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.movement_state = 0

        self.pressed_direction = vec(0, 0)
        self.current_direction = vec(0, 0)
        self.current_speed = vec(0, 0)
        self.target_direction = vec(0, 0)
        self.velocity = vec(0, 0)

        self.keys_pressed = pygame.key.get_pressed()
        self.collider = Collider()
        self.collision_objects = []
        

    def pressed(self, key: pygame.key):
        return self.keys_pressed[key]
    
    def just_pressed(self, key: pygame.key):
        return self.keys_pressed[key] and not self.keys_last[key]
    
    def just_released(self, key: pygame.key):
        return not self.keys_pressed[key] and self.keys_last[key]

    def update_keys(self):
        """
        Gets the current key states, compares them to the states of the last frame and updates corresponding lists accordingly
        """

        self.keys_last = copy.deepcopy(self.keys_pressed)
        self.keys_pressed = pygame.key.get_pressed()


    def get_target_direction(self):
        """
        Determines the direction the player wants to move to, by interpreting current and past inputs
        """

        def get_target_direction_for_axis(negative, positive, old):
            if not self.pressed(negative) and not self.pressed(positive):    
                return 0
            if self.just_pressed(negative):
                return -1
            if self.just_pressed(positive):
                return 1
            return old
        
        self.pressed_direction.x = get_target_direction_for_axis(LEFT, RIGHT, self.pressed_direction.x)
        self.pressed_direction.y = get_target_direction_for_axis(UP, DOWN, self.pressed_direction.y)

        if self.pressed_direction.length() != 0:
            self.target_direction = self.pressed_direction.normalize()
        else:
            self.target_direction = vec(0, 0)
            
    
    def get_current_direction_and_speed(self):
        """
        Determines where the player is currently moving towards
        """
        if self.velocity.length() != 0:
            self.current_direction = self.velocity.normalize()
        else:
            self.current_direction = vec(0, 0)

        self.current_speed = self.velocity.length()


    def control(self):
        """
        Determines what to do, in the player case interpret all the input
        """

        self.update_keys()
        self.get_target_direction()
        self.get_current_direction_and_speed()


    def update(self, delta):

        self.control()

        if self.target_direction.length() == 0 and self.current_direction.length() == 0:
            self.movement_state = STOPPED
        
        elif self.target_direction.length() != 0:
            self.movement_state = ACCELERATING
            self.velocity += ACCELERATION * self.target_direction
        else:
            self.movement_state = DECELERATING
            self.velocity = max(self.current_speed - DECELERATION, 0) * self.current_direction
        
        # Spielerkoordinate in tiles, + 0.5 um aus der Mitte des Charakters zu berechnen
        player_tile_x = round(self.position.x / TILE_SIZE + 0.5)
        player_tile_y = round(self.position.y / TILE_SIZE + 0.5)

        # Der Koordinateninvervall in der nach Kollision gecheckt werden soll
        collision_range_x = (pygame.math.clamp(player_tile_x - COLLISION_DETECTION_RANGE, 0, self.world.width - 1), pygame.math.clamp(player_tile_x + COLLISION_DETECTION_RANGE, 0, self.world.width - 1))
        collision_range_y = (pygame.math.clamp(player_tile_y - COLLISION_DETECTION_RANGE, 0, self.world.height - 1), pygame.math.clamp(player_tile_y + COLLISION_DETECTION_RANGE, 0,  self.world.height - 1))

        if DEBUGGING:
            for tile in self.collision_objects:
                if tile == None:
                    continue
                tile.untint()

        self.collision_objects = []

        # *tuple unpacks the values inside the tuple and uses them as paremeters for a function
        for tile_y in range(*collision_range_y):
            for tile_x in range(*collision_range_x):
                self.collision_objects.append(self.world.tile_map[tile_y][tile_x])

      
        for tile in self.collision_objects:

            if tile == None:
                continue

            if tile.has_collision == False:
                continue

            if DEBUGGING:
                tile.tint((100, 100, 100, 255))

            collisions = 0

            while self.collider.DynamicRectVsRect(self.rect, self.velocity, tile.rect) and collisions < 10:

                # TODO: A proper solution
                if self.collider.contact_normal == [0, 0]:
                    self.velocity.x *= 2
                    self.collider.DynamicRectVsRect(self.rect, self.velocity, tile.rect)


                self.velocity = self.collider.ResolveDynamicRectVsRect(self.velocity, self.collider.contact_time, self.collider.contact_normal)
                collisions += 1


        if self.velocity.length() != 0:
            self.velocity.clamp_magnitude_ip(0, MAX_SPEED)
        
        self.position += self.velocity

        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

        if self.just_pressed(pygame.K_r):
            self.position.x = 7 * TILE_SIZE
            self.position.y = 3 * TILE_SIZE


    def render(self, screen, camera):
        super().render(screen, camera)

        
        if DEBUGGING:

            color = (255, 0, 0)
            if self.movement_state == ACCELERATING:
                color = (0, 255, 0)
            
            relative_position_to_camera = (self.rect.centerx - camera.rect.x, self.rect.centery - camera.rect.y)

            pygame.draw.line(screen, color, relative_position_to_camera, relative_position_to_camera + self.velocity * 10)
            pygame.draw.line(screen, (0, 0, 255), relative_position_to_camera, relative_position_to_camera + self.target_direction * 10)
        