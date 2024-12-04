import pygame
from entities.tile import Tile

# ITile = interactive tile
class ITile(Tile):

    def __init__(self, range : pygame.Rect, action = None, params : any = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.range = range
        self.range.x += self.position.x
        self.range.y += self.position.y
        self.function = action
        self.params = params

    def update(self):
        if self.range.colliderect(self.world.player.rect):
            self.world.player.interactables.append(self)

    def render(self, screen, camera):
        super().render(screen, camera)

    def interact(self):
        if self.params is not None:
            self.function(self.params)
        else:
            self.function()
    
    def copy(self, x, y):
        return ITile(self.range, self.function, self.params, self.has_collision, self.sprite, x, y, self.rect.width, self.rect.height)