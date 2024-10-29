class World:

    def __init__(self, boundaries: tuple[int, int, int, int], tiles=[], creatures=[]):
        self.boundry_left, self.boundry_top, self.boundry_right, self.boundry_bottom = boundaries
        self.tiles = tiles
        self.creatures = creatures

    """
    def update(self, delta):

        for creature in self.creatures:
            creature.update(delta)
        
        for tile in self.tiles:
            tile.update(delta)
    
    def render(self):
        
        for creature in self.creatures:
            creature.render()
        
        for tile in self.tiles:
            tile.render() 
    """

    def register_creature(self, creature):
        self.creatures.append(creature)
    
    def unregister_creature(self, creature):
        self.creatures.remove(creature)