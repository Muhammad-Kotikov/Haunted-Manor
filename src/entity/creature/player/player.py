import pygame
import copy
from settings import *
from collider import Collider
from entity.creature.creature import Creature

MAX_SPEED = 3
ACCELERATION = MAX_SPEED / 5
DECELERATION = MAX_SPEED / 3
HARD_DECELERATION = MAX_SPEED / 2.5

# smaller values equal more smooth but thus slower turn (I think this can go above 1.0 ?)
TURN_FACTOR = 0.3

# Keymapping
LEFT = pygame.K_a
RIGHT = pygame.K_d
UP = pygame.K_w
DOWN = pygame.K_s

# Movement states
STOPPED = 0
ACCELERATING = 1
DECELERATING = 2
TURNING = 3


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

        # https://www.youtube.com/watch?v=YJB1QnEmlTs (An In-Depth look at Lerp, Smoothstep, and Shaping Functions)
        def smoothstep(t : float):
            v1 = t ** 2
            v2 = 1.0 - (1.0 - t) ** 2
            return pygame.math.lerp(v1, v2, t)

        self.control()

        new_direction = self.target_direction * TURN_FACTOR + self.current_direction * (1 - TURN_FACTOR)
        
        if new_direction.length() == 0:
            new_direction = self.target_direction
        else:
            new_direction.normalize_ip()

        if self.target_direction == -1 * self.current_direction:
            new_speed = max((self.current_speed - HARD_DECELERATION), 0)
            self.velocity = pygame.math.lerp(0, MAX_SPEED, smoothstep(new_speed / MAX_SPEED)) * self.current_direction
        
        elif self.target_direction.length() != 0 and new_direction.length() != 0:
            new_speed = min((self.current_speed + ACCELERATION), MAX_SPEED)
            self.velocity = pygame.math.lerp(0, MAX_SPEED, smoothstep(new_speed / MAX_SPEED)) * new_direction
        else:
            new_speed = max((self.current_speed - DECELERATION), 0)
            self.velocity = pygame.math.lerp(0, MAX_SPEED, smoothstep(new_speed / MAX_SPEED)) * self.current_direction
        
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

        """
        for tile_row in self.world.tile_map:
            for tile in tile_row:
                if tile == None:
                    continue
                tile.tint((255, 255, 255, 50), pygame.BLEND_RGBA_MULT)
        """

        # *tuple unpacks the values inside the tuple and uses them as paremeters for a function
        for tile_y in range(*collision_range_y):
            for tile_x in range(*collision_range_x):
                self.collision_objects.append(self.world.tile_map[tile_y][tile_x])

      
        for tile in self.collision_objects:

            if tile == None:
                continue

            if tile.has_collision == False:
                continue

            """
            if DEBUGGING:
                tile.tint((100, 100, 100, 255), pygame.BLEND_RGBA_MULT)
            """
                
            collisions = 0

            while self.collider.DynamicRectVsRect(self.rect, self.velocity, tile.rect) and collisions < 10:

                # TODO: A proper solution
                if self.collider.contact_normal == [0, 0]:
                    self.velocity.x *= 2
                    self.velocity.scale_to_length(MAX_SPEED)
                    self.collider.DynamicRectVsRect(self.rect, self.velocity, tile.rect)


                self.velocity = self.collider.ResolveDynamicRectVsRect(self.velocity, self.collider.contact_time, self.collider.contact_normal)
                collisions += 1


        #if self.velocity.length() != 0:
        #    self.velocity.clamp_magnitude_ip(0, MAX_SPEED)
        
        self.position += self.velocity

        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)


    def render(self, screen, camera):
        super().render(screen, camera)

        
        if DEBUGGING:

            color = (255, 0, 0)
            if self.movement_state == ACCELERATING:
                color = (0, 255, 0)
            
            relative_position_to_camera = (self.rect.centerx - camera.rect.x, self.rect.centery - camera.rect.y)

            pygame.draw.line(screen, color, relative_position_to_camera, relative_position_to_camera + self.velocity * 10)
            pygame.draw.line(screen, (0, 0, 255), relative_position_to_camera, relative_position_to_camera + self.target_direction * 10)
        