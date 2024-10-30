import pygame
import copy

from settings import *
from collider import Collider
from entity.creature.creature import Creature

MAX_SPEED = 16
ACCELERATION = MAX_SPEED / 6
DECELERATION = MAX_SPEED / 4
TURN_SPEED = DECELERATION

# Keymapping
LEFT = pygame.K_a
RIGHT = pygame.K_d
UP = pygame.K_w
DOWN = pygame.K_s

# Movement states
SLIDING = 0
ACCELERATING = 1
TURNING = 2

class Player(Creature):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        # needs to be initialized with something because the update methods expect values
        self.target_direction_x = 0
        self.target_direction_y = 0
        self.velocity_x = 0
        self.velocity_y = 0
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

        def get_target_direction_for_axis(negative, positive, old_target):
            if not self.pressed(negative) and not self.pressed(positive):    
                return 0
            if self.just_pressed(negative):
                return -1
            if self.just_pressed(positive):
                return 1
            return old_target
        
        self.target_direction_x = get_target_direction_for_axis(LEFT, RIGHT, self.target_direction_x)
        self.target_direction_y = get_target_direction_for_axis(UP, DOWN, self.target_direction_y)

    
    def get_current_direction(self):
        """
        Determines where the player is currently moving towards
        """

        self.currect_direction_x = (self.velocity_x > 0) - (self.velocity_x < 0)
        self.currect_direction_y = (self.velocity_y > 0) - (self.velocity_y < 0)
        self.currect_speed_x = abs(self.velocity_x)
        self.currect_speed_y = abs(self.velocity_y)


    def control(self):
        """
        Determines what to do, in the player case interpret all the input
        """

        self.update_keys()
        self.get_target_direction()
        self.get_current_direction()


    def update(self, delta_time):

        def calculate_velocity_for_axis(current_direction, target_direction, current_speed):

            if (current_direction == 0 and target_direction != 0) or (target_direction != 0 and current_direction == target_direction):
                # accelerating
                return min(current_speed + ACCELERATION, MAX_SPEED) * target_direction     
            elif target_direction != 0 and current_direction != target_direction:
                # turning
                return max((current_speed - TURN_SPEED) * current_direction, 0)
            # sliding/decelerating
            return max(current_speed - DECELERATION, 0) * current_direction

        self.control()

        # TODO: get FRAMERATE from main.py in here, can't import because that results in a deadlock of importing each other
        self.velocity_x = calculate_velocity_for_axis(self.currect_direction_x, self.target_direction_x, self.currect_speed_x) * delta_time * FRAMERATE * 0.001
        self.velocity_y = calculate_velocity_for_axis(self.currect_direction_y, self.target_direction_y, self.currect_speed_y) * delta_time * FRAMERATE * 0.001

        # Spielerkoordinate in tiles
        player_tile_x = self.rect.x // TILE_SIZE
        player_tile_y = self.rect.y // TILE_SIZE

        def limit(min_v, v, max_v):
            return max(min_v, min(max_v, v))
        
        #print(len(self.world.map[0]), "   ", len(self.world.map))

        # Der Koordinateninvervall in der nach Kollision gecheckt werden soll
        collision_range_x = (limit(0, player_tile_x - 2, len(self.world.map[0])), limit(0, player_tile_x + 2, len(self.world.map[0])))
        collision_range_y = (limit(0, player_tile_y - 2, len(self.world.map)), limit(0, player_tile_x + 2, len(self.world.map)))

        print(collision_range_x, "   ", collision_range_y)

        for tile_y in collision_range_y:
            for tile_x in collision_range_x:

                # Tile "holen" der nach Collision überprüft werden muss
                tile_id = self.world.map[tile_y][tile_x]
                
                if tile_id == 0:
                    continue

                tile = self.world.tilemap[tile_id]

                tile.rect.x = tile_x * TILE_SIZE
                tile.rect.y = tile_y * TILE_SIZE

                if self.collider.DynamicRectVsRect(self.rect, pygame.math.Vector2(self.velocity_x, self.velocity_y), tile.rect):

                    self.velocity_x , self.velocity_y = self.collider.ResolveDynamicRectVsRect(pygame.math.Vector2(self.velocity_x, self.velocity_y), self.collider.contact_time, self.collider.contact_normal)

                    # fixes corner collision (when hitting a corner we don't get a proper contact_normal whichs screws up the resoluve dynamic rect call)
                    if self.collider.contact_normal == [0, 0]:
                        
                        if self.velocity_x < self.velocity_y:
                            self.velocity_x = 0
                        else:
                            self.velocity_y = 0



        """
        for tile in self.world.tiles:
            if abs((self.rect.x + self.width / 2) - (tile.rect.x + tile.width / 2)) < TILE_SIZE * 2 and abs((self.rect.y + self.width / 2) - (tile.rect.y + tile.width / 2)) < TILE_SIZE * 2:

                if self.collider.DynamicRectVsRect(self.rect, pygame.math.Vector2(self.velocity_x, self.velocity_y), tile.rect):

                    self.velocity_x , self.velocity_y = self.collider.ResolveDynamicRectVsRect(pygame.math.Vector2(self.velocity_x, self.velocity_y), self.collider.contact_time, self.collider.contact_normal)

                    # fixes corner collision (when hitting a corner we don't get a proper contact_normal whichs screws up the resoluve dynamic rect call)
                    if self.collider.contact_normal == [0, 0]:
                        
                        if self.velocity_x < self.velocity_y:
                            self.velocity_x = 0
                        else:
                            self.velocity_y = 0
        """

        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # the velocity gets multiplied with delta before being mutated by the collision method call, so we revert it
        self.velocity_x /= delta_time
        self.velocity_y /= delta_time

    def render(self, screen):
        screen.blit(self.sprite, self.rect)