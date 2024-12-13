import pygame
import math
from entity import Entity

MAX_DISTANCE_TO_TARGET = 24
TIME_UNTIL_RECENTER = 45

vec = pygame.Vector2

class Camera:

    def __init__(self, rect : pygame.Rect, boundaries : pygame.Rect | None, target : Entity | None):
        self.position = vec(0, 0)
        if target:
            self.position = vec(target.rect.centerx - rect.width / 2, target.rect.centery - rect.height / 2)
        self.last_pos = self.position
        self.rect = rect
        self.target = target
        self.boundaries = boundaries
        self.timer = 0

    def update(self):

        # https://www.youtube.com/watch?v=YJB1QnEmlTs (An In-Depth look at Lerp, Smoothstep, and Shaping Functions)
        def smoothstep(t : float):
            v1 = t ** 2
            v2 = 1.0 - (1.0 - t) ** 2
            return pygame.math.lerp(v1, v2, t)

        new_pos = vec(0, 0)
        new_pos.x = self.target.rect.centerx - self.rect.width / 2
        new_pos.y = self.target.rect.centery - self.rect.height / 2

        if self.target:
            self.position.x = pygame.math.clamp(self.position.x, new_pos.x - MAX_DISTANCE_TO_TARGET, new_pos.x + MAX_DISTANCE_TO_TARGET)
            self.position.y = pygame.math.clamp(self.position.y, new_pos.y - MAX_DISTANCE_TO_TARGET, new_pos.y + MAX_DISTANCE_TO_TARGET)

        if self.target.velocity.length() == 0:
            self.timer += 1
        else:
            self.timer = 0
            
        
        if self.timer >= TIME_UNTIL_RECENTER:
            self.position.x = pygame.math.lerp(self.last_pos.x, new_pos.x, 0.08)
            self.position.y = pygame.math.lerp(self.last_pos.y, new_pos.y, 0.08)
            
        else:
            self.last_pos = self.position

        if self.boundaries:
            self.position.x = pygame.math.clamp(self.position.x, self.boundaries.x, self.boundaries.width - self.rect.width)
            self.position.y = pygame.math.clamp(self.position.y, self.boundaries.y, self.boundaries.height - self.rect.height)

        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def render(self, screen):
        pass