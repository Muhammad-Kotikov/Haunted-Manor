from entity import Entitiy
from abc import abstractmethod

class Creature(Entitiy):

    def __init__(self, hitpoints : int = 1):

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
    def draw(self):
        pass