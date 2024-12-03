from settings import *
from entities.creatures.player import *
from entities.tile import *
from entities.tiles.trap import *
from entities.creatures.enemy import *

CHUNK_SIZE = 16

class World:
    """
    explainations:

        there are "two kinds" of coordinates, the main difference is the "resolution" of the coordinates
        the scale is the TILE_SIZE. What does that mean? You take the smaller resolution coordinate, multiply
        it by the TILE_SIZE and get the higher resolution coordinate, so (with TILE_SIZE = 16):

        (3, 2) * TILE_SIZE = (48, 32)

        What's the use? The smaller resolution is "complete" and mathematically practical, the higher resolution
        is more useful for rendering and game logic.
        Mathematically practical means when I have a map which width equals 5 and height is 4,
        I know I have 20 tiles and complete means can just iterate through 0, 1, 2, 3, 4 and I always
        land on a tile without a gap. When I use the higher resolution I have to
        go though the coordinates 0, 16, 32, 48, 64 which is sort of annoying with loops
        Those numbers are however much more useful when drawing them on the screen or handling collisions

        so "Tile" Coordinates: smaller resolution discrete coordinates (always int)

        so "Rendering" Coordinates: higher resolution discrete/continous coordinates (int/float)

        =====

        there are "two kinds" of maps:

        Tile ID Map: this one only knows where a tile is (in tile coordinates) and what id it has
        (this is how you imagine a "stored" map (file), 0 for air/empty, 1 for a brick wall and so on)
        it does not however know what that tile's sprite is or what the collision rectangle look like
        it's basically a file with just a bunch of numbers, good for storing as it's pretty small
        and easy to edit (a. e. with TILED Editor)
        -> called id_map

        Tile Map: this one holds "proper" objects/instances of tiles, so it holds all the needed
        variables like screen coordinates, collision rectangle or the sprite and is
        (this is how you imagine the map in the game itself with its graphics and logic)
        but more information means more storage/processing space used
        -> tile_map
    """

    def __init__(self, file, spawnsheet):

        tile_id_map = self.read_map(file)
        self.width = len(tile_id_map[0])
        self.height = len(tile_id_map)
        self.creatures = []
        self.traps = []

        self.tile_map, creatures, traps = self.spawn_entities(tile_id_map, spawnsheet)

        for creature in creatures:
            self.register_creature(creature)

        for trap in traps:
            trap.world = self
            self.traps.append(trap)


    def read_map(self, file):
        """
        Wichter Kontext um diesen Code zu verstehen:
        .tmx Dateien sind wie folgt aufgebaut:
        5 Zeilen mit Informationen und Einstellungen zur GESAMTEN Karte
        Der Rest der Karte besteht aus sogenannten Chunks also "Stückchen" (der Karte)
        --> Diese 5 Zeilen überspringen wir komplett 

        Ein Chunk ist wie folgend aufgebaut:
        Die erste Zeile gibt die Chunkposition x, y und die Chunkgröße n
        --> davon nehmen wir die Chunkpositoin x, y mit, einmal um die gesamtgröße der Karte zu berechnen
            und später um die Chunks zu lesen und zu schreiben
        Dann n Zeilen mit jeweils n Zahlen die relativ zur Chunkposition angeben welche Tiles wo sind
        --> werden in self.tiles geschrieben
        Dann eine Schlusszeile (rein syntaktischer natur)
        --> übersprungen
        """

        data = self.read_map_file(file)
        boundaries = self.get_boundaries(data)

        return self.read_chunks(data, boundaries)
    

    @staticmethod
    def spawn_entities(entity_id_map, spawnsheet):
        """
        Turns a map of tile_ids into a map of Tile Class Objects
        """

        width = len(entity_id_map[0])
        height = len(entity_id_map)

        tile_map = [[None for _ in range(width)] for _ in range(height)]

        creatures = []
        traps = []

        for y, row in enumerate(entity_id_map):
            for x, entity_id in enumerate(row):
                if entity_id != 0:
                    entity = spawnsheet[entity_id]
                    xx = x * TILE_SIZE
                    yy = y * TILE_SIZE
                    if type(entity) == Player:
                        creatures.append(entity)
                        entity.position = vec(xx, yy)
                    elif type(entity) == Enemy:
                        creatures.append(entity)
                        entity.position = vec(xx, yy)
                    elif type(entity) == Creature:
                        creatures.append(entity)
                        entity.position = vec(xx, yy)
                    elif type(entity) == Trap:
                        traps.append(entity.copy(xx, yy))
                    elif type(entity) == Tile:   
                        tile_map[y][x] = entity.copy(xx, yy)

    
        return tile_map, creatures, traps


    @staticmethod
    def read_map_file(file):
        """
        Reads a given file and returns the content (stripped of some lines)
        """
        data = []
        for line in file:
            data.append(line.strip())

        return data[5:-3]


    @staticmethod
    def get_boundaries(data):
        """
        Determines the boundaries of a map when given it's (raw) id_map data, used to write the Tilemap
        """

        chunk_amount = (len(data) + 2) // (CHUNK_SIZE + 2)

        first_row = data[0].split("\"")
        first_x, first_y = int(first_row[1]), int(first_row[3])

        min_x = first_x
        max_x = first_x
        min_y = first_y
        max_y = first_y

        for chunk_index in range(chunk_amount):

            data_row = data[chunk_index * (CHUNK_SIZE + 2)].split("\"")
            chunk_x, chunk_y = int(data_row[1]), int(data_row[3])
            
            min_x = min(min_x, chunk_x)
            min_y = min(min_y, chunk_y)
            max_x = max(max_x, chunk_x + TILE_SIZE)
            max_y = max(max_y, chunk_y + TILE_SIZE)

        return (min_x, max_x, min_y, max_y)
    

    @staticmethod
    def read_chunks(data, boundaries):

        chunk_amount = (len(data) + 2) // (CHUNK_SIZE + 2)
        min_x, max_x, min_y, max_y = boundaries

        width = abs(min_x) + max_x
        height = abs(min_y) + max_y

        tiles = [[0 for _ in range(width)] for _ in range(height)]

        for chunk_index in range(chunk_amount):

            chunk_offset = chunk_index * (CHUNK_SIZE + 2)

            data_row = data[chunk_offset].split("\"")
            chunk_x, chunk_y = int(data_row[1]), int(data_row[3])

            for y in range(CHUNK_SIZE):
                row = data[chunk_offset + 1 + y].strip().split(",")
                for x in range(CHUNK_SIZE):
                    tiles[abs(min_y) + chunk_y + y][abs(min_x) + chunk_x + x] = int(row[x])
            
        return tiles


    def render(self, screen, camera):

        for tile_row in self.tile_map[camera.rect.y // TILE_SIZE: (camera.rect.y + camera.rect.height) // TILE_SIZE + 1]:
            for tile in tile_row[camera.rect.x // TILE_SIZE: (camera.rect.x + camera.rect.width) // TILE_SIZE + 1]:
                if tile is not None:
                    tile.render(screen, camera)

                    

        
        for trap in self.traps:
            trap.render(screen, camera)

        for creature in self.creatures:
            creature.render(screen, camera)


    def update(self, delta):

        for trap in self.traps:
            trap.update()

        for creature in self.creatures:
            creature.update(delta)



    def register_creature(self, creature):
        if type(creature) == Player:
            self.player = creature
        self.creatures.append(creature)
        creature.world = self
    

    def unregister_creature(self, creature):
        if type(creature) == Player:
            self.player = None       
        self.creatures.remove(creature)