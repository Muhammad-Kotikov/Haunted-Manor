from entity.entity import Entity
from abc import abstractmethod

class Creature(Entity):

    def __init__(self, hitpoints : int = 1):

        Entity.__init__(self)

        # hitpoints = maximale Lebenspunkte, health = momentane Lebenspunkte (z.B. nach dem man verletzt wurde)
        self.hitpoints = hitpoints
        self.health = hitpoints

    @abstractmethod
    def control(self):
        pass


    @abstractmethod
    def update(self, dt):
        pass


    @abstractmethod
    def render(self, screen):
        pass