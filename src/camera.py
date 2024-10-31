import pygame
from settings import DEBUGGING

vec = pygame.Vector2

class Camera:

    def __init__(self, rect : pygame.Rect, boundaries : pygame.Rect, target):
        self.position = vec(float(rect.centerx), float(rect.centery))
        self.rect = rect
        self.target = target
        self.boundaries = boundaries

    def update(self):

        # https://www.youtube.com/watch?v=YJB1QnEmlTs (An In-Depth look at Lerp, Smoothstep, and Shaping Functions)
        def smoothstep(t : float):
            v1 = t ** 2
            v2 = 1.0 - (1.0 - t) ** 2
            return pygame.math.lerp(v1, v2, t)


        if self.target:

            if self.target.velocity:
                offset_x = self.target.velocity.x * 30
                offset_y = self.target.velocity.y * 30
                weight = 0.15
            
            else:
                offset_x = 0
                offset_y = 0
                weight = 0.1
            
            
            self.camera_target_x = self.target.rect.centerx + offset_x
            self.camera_target_y = self.target.rect.centery + offset_y

            #distance_from_target_x = abs(self.rect.centerx - self.camera_target_x)
            #distance_from_target_y = abs(self.rect.centery - self.camera_target_y)

            self.position.x = pygame.math.lerp(self.position.x, self.camera_target_x, weight)
            self.position.y = pygame.math.lerp(self.position.y, self.camera_target_y, weight)

            self.rect.centerx = round(self.position.x)
            self.rect.centery = round(self.position.y)
    
        if self.boundaries:
            self.rect.x = pygame.math.clamp(self.rect.x, self.boundaries.x, self.boundaries.width - self.rect.width)
            self.rect.y = pygame.math.clamp(self.rect.y, self.boundaries.y, self.boundaries.height - self.rect.height)

    def render(self, screen):

        if DEBUGGING:
            pygame.draw.line(screen, (255, 255, 255), (self.rect.width / 2, self.rect.height / 2), (self.camera_target_x - self.rect.x, self.camera_target_y - self.rect.y))