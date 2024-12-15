from pygame import Rect
from entity import Entity

class Powerup(Entity):

    def __init__(self, range : Rect, effect, timer : int, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.range = range
        self.hit_box = Rect(range.left + self.position.x, range.top + self.position.y, range.width, range.height)
        self.effect = effect
        self.has_collision = False
        self.timer = timer
    

    def update(self):

        if self.world and self.world.player:

           if self.hit_box.colliderect(self.world.player.rect):
                self.effect()

                c = self.copy(self.position.x, self.position.y)
                c.world = self.world

                self.world.spawn_queue.append([self.timer, c])
                self.world.other.remove(self)

    def copy(self, x, y):
        return Powerup(self.range, self.effect, self.timer, self.sprite, x, y, self.rect.width, self.rect.height)
