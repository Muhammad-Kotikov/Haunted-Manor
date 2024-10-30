from settings import *
from entity.tile.tile import *

CHUNK_SIZE = 16

class World:

    def __init__(self, file, tilemap):

        self.map = self.read_map(file)
        self.creatures = []
        self.tiles = [] # nur zum vermeiden von collisoincodeerror
        self.tilemap = tilemap

        """
        for row in self.map:
            for tile in row:
                print(tile, end=" ")
            print()
        """


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

        data = self.read_file(file)
        boundaries = self.get_boundaries(data)

        return self.read_chunks(data, boundaries)


    def read_file(self, file):
        data = []
        for line in file:
            data.append(line.strip())

        return data[5:-3]


    def get_boundaries(self, data):

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
    

    def read_chunks(self, data, boundaries):

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


    def render(self, screen):

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile != 0:
                    self.tilemap[tile].position_x = x * TILE_SIZE
                    self.tilemap[tile].position_y = y * TILE_SIZE
                    self.tilemap[tile].render(screen)
        
        for creature in self.creatures:
            creature.render(screen)

    def update(self, delta):
        for creature in self.creatures:
            creature.update(delta)

    def register_creature(self, creature):
        self.creatures.append(creature)
    

    def unregister_creature(self, creature):
        self.creatures.remove(creature)