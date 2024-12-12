import pygame
from settings import Resolution, key_map
from tools import get_full_path

class Dialogue:

    FRAMES_PER_LETTER = 6
    

    def __init__(self, text = [], sprites = []):
        
        self.SMALL_FONT = pygame.font.Font(get_full_path("fonts/minecraft_font.ttf"), 7)
        self.phase = 0
        self.text = text
        self.text_amount = 0
        self.text_frame = 0
        self.sprites = sprites
        self.done = False
    

    def update(self):

        if self.phase == len(self.text):
            self.done = True
            return
        
        if self.text_amount < len(self.text[self.phase]):
            self.text_frame = (self.text_frame + 1) % self.FRAMES_PER_LETTER

        if self.text_frame == 0 and self.text_amount < len(self.text[self.phase]):
            self.text_amount += 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit = True
            if event.type == pygame.KEYDOWN and event.key == key_map["dialogue_next"]:
                if self.text_amount < len(self.text[self.phase]):
                    self.text_amount = len(self.text[self.phase])
                else:
                    self.phase += 1
                    self.text_frame = 0
                    self.text_amount = 0



    def render(self):

        if self.phase < len(self.sprites):
            self.screen.blit(self.sprites[self.phase], (Resolution.WIDTH // 2 - self.sprites[self.phase].get_width() // 2, 50))
            label = self.SMALL_FONT.render(self.text[self.phase][:self.text_amount], False, (255, 255, 255))
            self.screen.blit(label, (50, 300))


        