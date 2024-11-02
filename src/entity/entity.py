import pygame
from settings import TILE_SIZE
from abc import abstractmethod

vec = pygame.math.Vector2

class Entity:

    def __init__(self, sprite : pygame.sprite, x : float = 0, y : float  = 0, width : int = TILE_SIZE, height : int = TILE_SIZE):

        self.position = vec(x, y)
        self.sprite = sprite
        self.original = self.sprite.copy()
        self.rect = pygame.Rect(x, y, width, height)


    def update(self):
        pass


    def render(self, screen, camera):
        screen.blit(self.sprite, (self.rect.x - camera.rect.x, self.rect.y - camera.rect.y))
    

    def tint(self, color, flag):

        # https://stackoverflow.com/questions/57962130/how-can-i-change-the-brightness-of-an-image-in-pygame
        self.sprite = self.original.copy()
        self.sprite.fill(color, special_flags=flag)
        
    
    def untint(self):
        
        self.sprite = self.original


