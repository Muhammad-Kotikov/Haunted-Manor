from entity import Entity
from abc import abstractmethod
import pygame

INVUNERABLE_FRAMES = 60

class Creature(Entity):

    def __init__(self, hitpoints : int = 1, *args, **kwargs):

        super().__init__(*args, **kwargs)
        #self.world = world

        # hitpoints = maximale Lebenspunkte, health = momentane Lebenspunkte (z.B. nach dem man verletzt wurde)
        self.hitpoints = hitpoints
        self.health = hitpoints

        self.invunerable = False
        self.i_frames_left = 0
        #world.register_creature(self)


    @abstractmethod
    def control(self):
        pass


    @abstractmethod
    def update(self, dt):
        pass


    def render(self, screen, camera):
        super().render(screen, camera)

    def hit(self, damage):

        if self.invunerable:
            return

        self.health -= damage

        if self.health <= 0:
            self.die()
            return

        self.invunerable = True
        self.i_frames_left = INVUNERABLE_FRAMES
        self.tint((255, 255, 255, 80), pygame.BLEND_RGB_ADD)
        

    def die(self):
        self.world.unregister_creature(self)


    def copy(self, x, y):
        return Creature(self.hitpoints, self.sprite, x, y, self.rect.width, self.rect.height)