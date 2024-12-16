from game import *  
import pygame
from settings import *
import os

class Intro:
    def __init__(self):
        self.intro_surface = pygame.Surface((Resolution.WIDTH * TILE_SIZE, Resolution.HEIGHT * TILE_SIZE))
        self.frames_path = "rsc/sprites/videos/intro"
        self.frames = sorted(
            [
                os.path.join(self.frames_path, f)
                for f in os.listdir(self.frames_path)
                if f.endswith(".png")
            ]
        )

        self.clock      = pygame.time.Clock()
        self.running    = True
        self.index      = 0

    
    def render_intro(self):
        while self.running:
            if self.index < len(self.frames):
                frame = pygame.image.load(self.frames[self.index]).convert_alpha()

                censored_frame = self.apply_censorship(frame)

                frame_rect = censored_frame.get_rect()
                frame_width, frame_height = frame_rect.width, frame_rect.height

                x_offset = (Display.WIDTH - frame_width) // 2
                y_offset = (Display.HEIGHT - frame_height) // 2

                self.intro_surface.blit(censored_frame, (x_offset, y_offset))

                self.index += 1
                self.clock.tick(19)

            else:
                self.running = False

    def apply_censorship(self, frame):
        censored_frame = frame.copy()
        rect = pygame.Rect(50, 50, 100, 100)
        pygame.draw.rect(censored_frame, (0, 0, 0), rect)
        return censored_frame