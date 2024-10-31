from entity.entity import Entity

class Tile(Entity):

    def __init__(self, has_collision : bool = False, *args, **kwargs):

        self.has_collision = has_collision

        super().__init__(*args, **kwargs)