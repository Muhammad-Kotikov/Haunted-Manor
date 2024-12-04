import pygame
from settings import TILE_SIZE

vec = pygame.math.Vector2

class Entity:

    def __init__(self, sprite : pygame.sprite, x : float = 0, y : float  = 0, width : int = TILE_SIZE, height : int = TILE_SIZE):

        self.position = vec(x, y)
        self.sprite = sprite
        self.original = self.sprite.copy()
        self.rect = pygame.Rect(x, y, width, height)


    def update(self):
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)


    def render(self, screen, camera):
        screen.blit(self.sprite, (round(self.rect.x - camera.rect.x), round(self.rect.y - camera.rect.y)))
    

    def tint(self, color, flag):

        # https://stackoverflow.com/questions/57962130/how-can-i-change-the-brightness-of-an-image-in-pygame
        self.sprite = self.original.copy()
        self.sprite.fill(color, special_flags=flag)
        
    
    def untint(self):
        
        self.sprite = self.original
