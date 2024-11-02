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

            offset = vec(0, 0)

            if self.target.velocity:
                offset.x = self.target.velocity.x * 30
                offset.y = self.target.velocity.y * 30
            
            
            self.camera_target = self.target.rect.center + offset

            self.position.x = pygame.math.lerp(self.position.x, self.camera_target.x, 0.05)
            self.position.y = pygame.math.lerp(self.position.y, self.camera_target.y, 0.05)

            self.rect.centerx = round(self.position.x)
            self.rect.centery = round(self.position.y)
    
        if self.boundaries:
            self.rect.x = pygame.math.clamp(self.rect.x, self.boundaries.x, self.boundaries.width - self.rect.width)
            self.rect.y = pygame.math.clamp(self.rect.y, self.boundaries.y, self.boundaries.height - self.rect.height)

    def render(self, screen):

        pass
        #if DEBUGGING:
        #    pygame.draw.line(screen, (255, 255, 255), (self.rect.width / 2, self.rect.height / 2), (self.camera_target.x - self.rect.x, self.camera_target.y - self.rect.y))