import pygame
import copy
from settings import *
from entities.creature import Creature
from collider import * 

# Keymapping
LEFT = pygame.K_a
RIGHT = pygame.K_d
UP = pygame.K_w
DOWN = pygame.K_s

IDLE = 0
RUNNING = 1
STOPPING = 2

MAX_SPEED = 1.5
ACCELERATION = MAX_SPEED / 6
DECELERATION = MAX_SPEED / 4

COLLISION_DETECTION_RANGE = 2

vec = pygame.Vector2

class Player(Creature):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.collider = SimpleCollider()

        self.last_left = 0
        self.last_right = 0
        self.last_up = 0
        self.last_down = 0

        self.interactables = []

        self.movement_state = -1

        self.pressed_direction = vec(0, 0)
        self.current_direction = vec(0, 0)
        self.current_speed = vec(0, 0)
        self.target_direction = vec(0, 0)
        self.velocity = vec(0, 0)

        self.keys_pressed = pygame.key.get_pressed()

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

        def get_target_direction_for_axis(neg, pos, last_neg, last_pos):
            """
            Given two buttons and the frame length since they were last pressed, determines the direction the player intents to move
            """

            # nothing pressed
            if not self.pressed(neg) and not self.pressed(pos):
                return 0
            
            # only negative pressed
            if self.pressed(neg) and not self.pressed(pos):
                return -1
            
            # only positive pressed
            if not self.pressed(neg) and self.pressed(pos):
                return 1
            
            # both pressed but negative was pressed later
            elif last_neg < last_pos:
                return -1
            
            # both pressed at same time or positive later
            else:
                return 1
            
        def count_last(button, counter):
            # if the button was just pressed, the last press is 0 frames ago
            if self.just_pressed(button):
                return 0
            else:
                # else just count up
                return counter + 1
            
        pressed_direction = vec(0, 0)
            
        self.last_left = count_last(LEFT, self.last_left)
        self.last_right = count_last(RIGHT, self.last_right)
        self.last_up = count_last(UP, self.last_up)
        self.last_down = count_last(DOWN, self.last_down)
        
        pressed_direction.x = get_target_direction_for_axis(LEFT, RIGHT, self.last_left, self.last_right)
        pressed_direction.y = get_target_direction_for_axis(UP, DOWN, self.last_left, self.last_right)

        if self.pressed_direction.length() != 0:
            pressed_direction.normalize()
        
        self.target_direction = pressed_direction
        

    def control(self):
        """
        Determines what to do, in the player case interpret all the input
        """

        self.update_keys()
        self.get_target_direction()


    def move(self):


        # https://www.youtube.com/watch?v=YJB1QnEmlTs (An In-Depth look at Lerp, Smoothstep, and Shaping Functions)
        def smoothstep(t : float):
            v1 = t ** 2
            v2 = 1.0 - (1.0 - t) ** 2
            return pygame.math.lerp(v1, v2, t)
        

        if self.target_direction != vec(0, 0):
            self.movement_state = RUNNING
            new_speed = min((self.velocity.length() + ACCELERATION * self.delta_time), MAX_SPEED)
            direction = self.target_direction
        

        elif self.target_direction == vec(0, 0) and self.velocity.length() > 0:
            self.movement_state = STOPPING
            new_speed = max((self.velocity.length() - DECELERATION * self.delta_time), 0)
            direction = self.velocity.normalize()


        else:
            self.movement_state = IDLE
            new_speed = 0
            direction = vec(0, 0)


        """ uncomment when player ignores max speed, math.lerp "soft clamps" it anyway so not really needed """
        if self.velocity.length() > 0:
            self.velocity.clamp_magnitude_ip(MAX_SPEED)
        

        self.velocity = pygame.math.lerp(0, MAX_SPEED, smoothstep(new_speed / MAX_SPEED)) * direction


      

    def slide(self):

        
        # Spielerkoordinate in tiles, (aus der Mitte des Charakters) zu berechnen
        player_tile_x = round(self.rect.centerx / TILE_SIZE)
        player_tile_y = round(self.rect.centery / TILE_SIZE)

        # Der Koordinateninvervall in der nach Kollision gecheckt werden soll
        collision_range_x = (pygame.math.clamp(player_tile_x - COLLISION_DETECTION_RANGE, 0, self.world.width - 1), pygame.math.clamp(player_tile_x + COLLISION_DETECTION_RANGE, 0, self.world.width - 1))
        collision_range_y = (pygame.math.clamp(player_tile_y - COLLISION_DETECTION_RANGE, 0, self.world.height - 1), pygame.math.clamp(player_tile_y + COLLISION_DETECTION_RANGE, 0,  self.world.height - 1))

        if DEBUGGING and SHOW_COLLISION_RANGE:
            for tile in self.collision_objects:
                if tile == None:
                    continue
                tile.untint()

        self.collision_objects = []

        # "*tuple" unpacks the values inside the tuple and uses them as paremeters for a function
        for tile_y in range(*collision_range_y):
            for tile_x in range(*collision_range_x):

                if self.world.tile_map[tile_y][tile_x] != None and self.world.tile_map[tile_y][tile_x].has_collision == True:

                    self.collision_objects.append(self.world.tile_map[tile_y][tile_x])

      
        for tile in self.collision_objects:
            
            if DEBUGGING and SHOW_COLLISION_RANGE:
                tile.tint((100, 100, 100, 255), pygame.BLEND_RGBA_MULT)

        self.position += self.velocity

        self.collider.collide_with_wall(self, self.collision_objects)
        


            
        

    
    def move_and_slide(self):



        # calculate velocity (without collision) based on player intent
        self.move()

        # check collision and slide character along walls
        self.slide()

        # change player position vector
        

        # move the player rectangle (used for sprite and collisoin, integer)
        #self.rect.x = round(self.position.x)
        #self.rect.y = round(self.position.y)
    


    def update(self, delta):


        self.delta_time = delta

        """ tint all tiles in the map
        for tile_row in self.world.tile_map:
            for tile in tile_row:
                if tile == None:
                    continue
                tile.tint((255, 255, 255, 50), pygame.BLEND_RGBA_MULT)
        """

        # get player intent
        self.control()

        # move, collide and slide the character
        self.move_and_slide()

        if self.invunerable:
            self.i_frames_left -= 1

        if self.i_frames_left <= 0:
            self.invunerable = False
            self.untint()

        if self.just_pressed(pygame.K_e) and len(self.interactables) > 0:
            self.interactables[0].interact()
        self.interactables.clear()



    def render(self, screen, camera):
        super().render(screen, camera)

        
        if DEBUGGING and SHOW_MOVEMENT_VECTORS:

            relative_position_to_camera = (self.rect.centerx - camera.rect.x, self.rect.centery - camera.rect.y)

            velocity_normalized = vec(0, 0) if self.velocity.length() == 0 else self.velocity.normalize()


            pygame.draw.line(screen, (0, 0, 255), relative_position_to_camera, relative_position_to_camera + self.target_direction * 30)
            pygame.draw.line(screen, (255, 0, 0), relative_position_to_camera, relative_position_to_camera + velocity_normalized * 30)
    
