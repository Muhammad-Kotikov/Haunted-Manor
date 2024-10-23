import pygame
from collider import Collider
from entity.creature.creature import Creature

MAX_SPEED = 0.2
ACCELERATION = MAX_SPEED / 5
DECELERATION = MAX_SPEED / 3


# Keymappings (the ones from pygame break when converting into a list)
LEFT = 4
RIGHT = 7
UP = 26
DOWN = 22

# Movement states
SLIDING = 0
ACCELERATING = 1
TURNING = 2

class Player(Creature):

    def __init__(self, world):

        Creature.__init__(self)

        self.world = world

        self.target_direction_x = 0
        self.target_direction_y = 0

        self.velocity_x = 0
        self.velocity_y = 0

        self.collider = Collider()

        ### TEST ###
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        ############

        # needs to be initialized with something to avoid errors with empty lists in update_keys()
        self.keys_pressed = list(pygame.key.get_pressed())

    def update_keys(self):
        """
        Gets the current key states, compares them to the states of the last frame and updates corresponding lists accordingly
        """

        self.keys_last = self.keys_pressed.copy()
        self.keys_pressed = list(pygame.key.get_pressed())
        self.keys_just_pressed = []

        for key_pressed, key_last_pressed in zip(self.keys_pressed, self.keys_last):
            self.keys_just_pressed.append(key_pressed and not key_last_pressed)


    def get_target_direction(self):
        """
        Determines the direction the player wants to move to, by interpreting current and past inputs
        """

        def get_target_direction_for_axis(direction, complementary_direction, old_target):
            if not self.keys_pressed[direction] and not self.keys_pressed[complementary_direction]:    
                return 0
            if self.keys_just_pressed[direction]:
                return -1
            if self.keys_just_pressed[complementary_direction]:
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
                return max((current_speed - DECELERATION - ACCELERATION) * current_direction, 0)
            # sliding/decelerating
            return max(current_speed - DECELERATION, 0) * current_direction

        self.control()

        self.velocity_x = calculate_velocity_for_axis(self.currect_direction_x, self.target_direction_x, self.currect_speed_x)
        self.velocity_y = calculate_velocity_for_axis(self.currect_direction_y, self.target_direction_y, self.currect_speed_y)
        # TODO: SCHRÄGES MOVEMENT

        for tile in self.world:
            if abs((self.rect.x + self.width / 2) - (tile.rect.x + tile.width / 2)) < 64 and abs((self.rect.y + self.width / 2) - (tile.rect.y + tile.width / 2)) < 64:
                print("close", end=" ")
                if self.collider.DynamicRectVsRect(self.rect, pygame.math.Vector2(self.velocity_x, self.velocity_y), tile.rect):
                    print("hit", end=" ")
                self.velocity_x, self.velocity_y = self.collider.ResolveDynamicRectVsRect(pygame.math.Vector2(self.velocity_x, self.velocity_y), self.collider.contact_time, self.collider.contact_normal)
                print("")
            else:
                print("far")

        self.rect.x += self.velocity_x * delta_time 
        self.rect.y += self.velocity_y * delta_time 

    def render(self, screen):
        screen.blit(self.image, self.rect)