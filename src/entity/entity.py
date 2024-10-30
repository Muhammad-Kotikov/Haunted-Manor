import pygame

class Entity:

    def __init__(self, sprite : str = "", position_x : float = 0.0, position_y : float = 0.0, width : int = 16, height : int = 16):

        self.width = width
        self.height = height

        self.rect = pygame.Rect(position_x, position_y, width, height)
        
        self.sprite = sprite



