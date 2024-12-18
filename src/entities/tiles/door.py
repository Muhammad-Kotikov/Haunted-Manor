import pygame
from entities.tile import *
from tools import play_soundeffect 

class Door(Tile):

    def __init__(self, range : pygame.Rect, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.range = range.copy()
        self.range.x += self.position.x
        self.range.y += self.position.y
    
    def update(self):
        if not self.world.player:
            return
        if self.range.colliderect(self.world.player.rect):
            self.world.player.interactables.append(self)

    def render(self, screen, camera):
        if self.has_collision:
            super().render(screen, camera)

    def interact(self):

        # toggle own collision
        if self.world.player and not self.rect.colliderect(self.world.player.rect):
            self.has_collision = not self.has_collision
        
        # toggle neighboring doors collision
        for tile in self.world.interactables:
           if type(tile) == Door:
                if self.range.colliderect(tile.rect):
                    tile.has_collision = self.has_collision
                    play_soundeffect('rsc/sounds/open_door.mp3', 0.3)
                else:
                    play_soundeffect('rsc/sounds/close_door.mp3', 0.3)    
    def copy(self, x, y):
        return Door(self.range, self.has_collision, self.sprite, x, y, self.rect.width, self.rect.height)