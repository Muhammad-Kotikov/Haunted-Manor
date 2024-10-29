from entity.entity import Entity
from abc import abstractmethod

class Creature(Entity):

    def __init__(self, world, hitpoints : int = 1, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.world = world

        # hitpoints = maximale Lebenspunkte, health = momentane Lebenspunkte (z.B. nach dem man verletzt wurde)
        self.hitpoints = hitpoints
        self.health = hitpoints
        world.register_creature(self)

    @abstractmethod
    def control(self):
        pass


    @abstractmethod
    def update(self, dt):
        pass


    @abstractmethod
    def render(self, screen):
        pass

    def die(self):
        self.world.creatures.remove(self)