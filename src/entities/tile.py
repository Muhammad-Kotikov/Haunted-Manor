from entity import Entity

class Tile(Entity):

    def __init__(self, has_collision : bool = False, *args, **kwargs):

        self.has_collision = has_collision

        super().__init__(*args, **kwargs)
    

    def copy(self, x, y):

        return Tile(self.has_collision, self.sprite, x, y, self.rect.width, self.rect.height)
    
    