import pygame
import input

from settings import *
from entities.creature import Creature

vec = pygame.Vector2

class Player(Creature):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.input = input.InputHander(self)
        self.interactables = []
        self.tint_objects = []
        self.speed_boost_duration = 0
        self.keys = 0

    
    def control(self):
        """
        Determines what to do, in the player case interpret all the input
        """

        self.input.update_keys()
        #self.target_direction = self.input.get_target_direction()

    
    def update(self, delta):

        if self.speed_boost_duration > 0:
            self.acc_factor = 2
            self.spd_fac = 3
        else:
            self.acc_fac = 1
            self.spd_fac = 1

        super().update(delta)

        self.interactables.clear()
        for interactable in self.world.interactables:
            if hasattr(interactable, "range") and self.rect.colliderect(interactable.range):
                self.interactables.append(interactable)


        if self.input.just_pressed(key_map["interact"]) and len(self.interactables) > 0:
            self.interactables[0].interact()
        
        self.speed_boost_duration -= 1



    def render(self, screen, camera):
        super().render(screen, camera)
        
        if options['debugging'] and options['movement_vectors']:

            relative_position_to_camera = (self.rect.centerx - camera.rect.x, self.rect.centery - camera.rect.y)

            velocity_normalized = vec(0, 0) if self.velocity.length() == 0 else self.velocity.normalize()

            if self.target_direction.length() > 0 :
                pygame.draw.line(screen, (0, 0, 255), relative_position_to_camera, relative_position_to_camera + self.target_direction.normalize() * 10)
            
            pygame.draw.line(screen, (255, 0, 0), relative_position_to_camera, relative_position_to_camera + velocity_normalized * 20)

        if options['debugging'] and options['collision_range']:

            for tinted_object in self.tint_objects:
                tinted_object.untint()

            # Spielerkoordinate in tiles, (aus der Mitte des Charakters) zu berechnen
            creature_tile_x = round(self.rect.centerx / TILE_SIZE)
            creature_tile_y = round(self.rect.centery / TILE_SIZE)

            # Der Koordinateninvervall in der nach Kollision gecheckt werden soll
            collision_range_x = (pygame.math.clamp(creature_tile_x - self.COLLISION_DETECTION_RANGE, 0, self.world.width - 1), pygame.math.clamp(creature_tile_x + self.COLLISION_DETECTION_RANGE, 0, self.world.width - 1))
            collision_range_y = (pygame.math.clamp(creature_tile_y - self.COLLISION_DETECTION_RANGE, 0, self.world.height - 1), pygame.math.clamp(creature_tile_y + self.COLLISION_DETECTION_RANGE, 0,  self.world.height - 1))

            self.tint_objects = []

            # "*tuple" unpacks the values inside the tuple and uses them as paremeters for a function
            for tile_y in range(*collision_range_y):
                for tile_x in range(*collision_range_x):
                    if self.world.tile_map[tile_y][tile_x] != None and self.world.tile_map[tile_y][tile_x].has_collision == True:
                        self.tint_objects.append(self.world.tile_map[tile_y][tile_x])
                        self.world.tile_map[tile_y][tile_x].tint((100, 100, 100, 255), pygame.BLEND_RGBA_MULT)
            
            for interactable in self.interactables:
                if interactable.has_collision:
                    self.tint_objects.append(interactable)
                    interactable.tint((100, 100, 100, 255), pygame.BLEND_RGBA_MULT)
    
