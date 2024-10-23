from entity.entity import Entity

class Tile(Entity):

    def update(delta):
        pass

    def render(self, screen):
        screen.blit(self.sprite, (self.position_x, self.position_y))