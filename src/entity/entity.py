import pygame

class Entitiy:

    def __init__(self, spritepath : str, position_x : int = 0, position_y : int = 0, width : int = 16, height : int = 16):
        self.position_x = position_x
        self.position_y = position_y
        self.width = width
        self.height = height

        self.rect = pygame.Rect(position_x, position_y, width, height)
        
        try:
            # das ".convert" sorgt für bessere Performanz laut Tutorial und Pygame docs
            # muss man nicht verstehen xD, ".convert_alpha für Bilder mit Alpha Kanal (Tranzparenz für normal Sterbliche)
            self.sprite = pygame.image.load(spritepath).convert_alpha()
        except:
            print("ERROR Loading sprite for entity")



