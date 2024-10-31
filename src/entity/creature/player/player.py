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

        """
        self.current_direction.x = (self.velocity.x > 0) - (self.velocity.x < 0)
        self.current_direction.y = (self.velocity.y > 0) - (self.velocity.y < 0)
        self.current_speed.x = abs(self.velocity.x)
        self.current_speed.y = abs(self.velocity.y)
        """

    def control(self):
        """
        Determines what to do, in the player case interpret all the input
        """

        self.update_keys()
        self.get_target_direction()
        self.get_current_direction_and_speed()


    def update(self, delta):

        """
        def calculate_velocity_for_axis(current_direction, target_direction, current_speed):

            if (current_direction == vec.zero and target_direction != 0) or (target_direction != 0 and current_direction == target_direction):
                # accelerating
                return min(current_speed + ACCELERATION, MAX_SPEED) * target_direction     
            elif target_direction != 0 and current_direction != target_direction:
                # turning
                return max((current_speed - TURN_SPEED), 0) * current_direction
            # sliding/decelerating
            return max(current_speed - DECELERATION, 0) * current_direction
        """

        self.control()


        if self.target_direction.length() == 0 and self.current_direction.length() == 0:
            self.movement_state = STOPPED
        
        elif self.target_direction.length() == 0:
            self.movement_state = DECELERATING
            self.velocity = max(self.current_speed - DECELERATION, 0) * self.current_direction
            #print("decelerating")
        else:
            self.movement_state = ACCELERATING
            self.velocity += ACCELERATION * self.target_direction
            #print("accelerating")
        
        # Spielerkoordinate in tiles
        player_tile_x = round(self.position.x / TILE_SIZE) 
        player_tile_y = round(self.position.y / TILE_SIZE)
        
        def clamp(min_v, v, max_v):
            return max(min_v, min(max_v, v))

        # Der Koordinateninvervall in der nach Kollision gecheckt werden soll
        collision_range_x = (clamp(0, player_tile_x - 2, self.world.width), clamp(0, player_tile_x + 2, self.world.width))
        collision_range_y = (clamp(0, player_tile_y - 2, self.world.height) , clamp(0, player_tile_y + 2, self.world.height))

        # *tuple unpacks the values inside the tuple and uses them as paremeters for a function
        for tile_y in range(*collision_range_y):
            for tile_x in range(*collision_range_x):

                tile = self.world.tile_map[tile_y][tile_x]

                if tile == None:
                    continue

                #tile.rect.x = tile_x * TILE_SIZE
                #tile.rect.y = tile_y * TILE_SIZE

                if self.collider.DynamicRectVsRect(self.rect, self.velocity, tile.rect):

                    self.velocity = self.collider.ResolveDynamicRectVsRect(self.velocity, self.collider.contact_time, self.collider.contact_normal)

                    # fixes corner collision (when hitting a corner we don't get a proper contact_normal whichs screws up the resoluve dynamic rect call)
                    if self.collider.contact_normal == [0, 0]:
                        pass
                    
                        
                    

        if self.velocity.length() != 0:
            self.velocity.clamp_magnitude_ip(0, MAX_SPEED)
        
        #print(self.velocity)

        self.position += self.velocity

        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

        if self.just_pressed(pygame.K_r):
            self.position.x = 0
            self.position.y = 0


    def render(self, screen):
        screen.blit(self.sprite, self.rect)
        color = (255, 0, 0)
        if self.movement_state == ACCELERATING:
            color = (0, 255, 0)
            
        pygame.draw.line(screen, color, self.rect.center, self.rect.center + self.velocity * 10)
        pygame.draw.line(screen, (0, 0, 255), self.rect.center, self.rect.center + self.target_direction * 10)