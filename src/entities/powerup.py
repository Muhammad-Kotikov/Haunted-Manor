from pygame import Rect
from entity import Entity

class Powerup(Entity):

    def __init__(self, range : Rect, effect, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.range = range
        range.left += self.position.x
        range.top += self.position.y
        self.effect = effect
        self.has_collision = False
    

    def update(self):

        if self.world and self.world.player:
           if self.range.colliderect(self.world.player.rect):
                self.effect()
                self.world.other.remove(self)

    def copy(self, x, y):
        return Powerup(self.range, self.effect, self.sprite, x, y, self.rect.width, self.rect.height)
