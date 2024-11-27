import pygame

class HUD:

    def __init__(self, target, health_sprite, empty_health_sprite):

        self.target = target
        self.health_sprite = health_sprite
        self.empty_health_sprite = empty_health_sprite

    

    def render(self, screen):

        if self.target == None:
            return
        
        offset_x = 2
        offset_y = 2
        distance_x = 16

        for x in range(self.target.health):
            screen.blit(self.health_sprite, (offset_x + distance_x * x, offset_y))
        
        for x in range(self.target.health, self.target.hitpoints):
            screen.blit(self.empty_health_sprite, (offset_x + distance_x * x, offset_y))