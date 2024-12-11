import pygame

class HUD:

    def __init__(self, target, health_sprite, empty_health_sprite):

        self.target = target
        self.health_sprite = health_sprite
        self.empty_health_sprite = empty_health_sprite
        self.SMALL_FONT = pygame.font.Font("./rsc/fonts/minecraft_font.ttf", 7)

    

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

        if len(self.target.interactables) > 0:
            label = self.SMALL_FONT.render("Press E to interact", 0, (255, 255, 255))
            screen.blit(label, (screen.get_width() / 2 - label.get_width() / 2, screen.get_height() * 0.8))
        