from game import *
import pygame
from settings import *
import os

class PauseMenu:
    def __init__(self):
        # Bildschirmoberfläche holen
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font('rsc/fonts/SpecialElite-Regular.ttf', 18)
        self.pause_surface = pygame.Surface((Resolution.WIDTH * TILE_SIZE, Resolution.HEIGHT * TILE_SIZE))
        self.paused = True
        self.running = True  # Variable für die Steuerung der Hauptschleife

    def draw_pausemenu(self):
        # Text "Game Paused" zentrieren und zeichnen
        pause_text = self.font.render("Game Paused", True, (255, 255, 255))
        self.pause_surface.blit    

    def render_pause_screen(self):
        self.pause_surface.fill((0, 0, 0))
        self.draw_pausemenu()

    def update_pausemenu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                    