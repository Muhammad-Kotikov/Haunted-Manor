import pygame
from settings import TILE_SIZE

vec = pygame.math.Vector2

class Entity:

    def __init__(self, sprite : pygame.sprite, x : float = 0, y : float  = 0, width : int = TILE_SIZE, height : int = TILE_SIZE):

        self.position = vec(x, y)
        self.sprite = sprite
        self.rect = pygame.Rect(x, y, width, height)


    def update(self):
        pass


    def render(self, screen):
        screen.blit(self.sprite, (self.rect.x, self.rect.y))



