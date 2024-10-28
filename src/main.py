import pygame
import os

from entity.creature.player.player import Player
from entity.tile.tile import Tile
from world import World

# https://www.youtube.com/watch?v=AY9MnQ4x3zk / Mua / 23.09.24
# Danke Muha / 25.09.24

# Titel wird über dem Fenster angezeigt
TITLE = "Haunted Manor"

# TILE_SIZE ist die Pixelgröße eines Feldes im Spiel
TILE_SIZE = 16

# WIDTH und HEIGHT geben an wie viele Felder in vertikel und horizontal in den Bildschirm reinpassen
WIDTH = 20
HEIGHT = 15

# So oft läuft die Spielschleife pro Sekunde, das heißt es wird FRAMERATE oft bspw. die Kollision gecheckt,
# so viele Bilder werden angezeigt und so oft kann sich etwas auf dem Bildschirm bewegen
FRAMERATE = 60

running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SCALED)
pygame.display.set_caption(TITLE)

def get_rsc():
    """
    Returns the Gamefolder
    """
    # os.path.dirname() is weird
    return os.path.dirname(os.path.dirname(__file__))

def get_sprite(filename: str):
    return os.path.join(get_rsc(), f'rsc/sprites/{filename}')

def get_map(filename: str):
    return os.path.join(get_rsc(), f'rsc/maps/{filename}')

def init():
    pygame.init()
    pygame.mixer.init()
    

def update(delta):

    for creature in world.creatures:
        creature.update(delta)

def render():
    # Malfläche zurücksetzen
    screen.fill((0, 0, 0))

    for tile in world.tiles:
        tile.render(screen)

    for creature in world.creatures:
        creature.render(screen)

    # Malfläche anzeigen
    pygame.display.flip()


init()

brick1 = Tile(get_sprite("brick.png"), 128, 128, 16, 16)
brick2 = Tile(get_sprite("brick.png"), 128, 112, 16, 16)
brick3 = Tile(get_sprite("brick.png"), 112, 112, 16, 16)
world = World((0, 0, 32, 32), [brick1, brick2, brick3])
player = Player(world, 10, get_sprite("sabrina.png"), 0, 0, 23, 36)

delta = 1

while running:

    for event in pygame.event.get():

        # Fenster schließbar machen
        if event.type == pygame.QUIT:
            running = False

    update(delta)
    render()
        
    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    delta = clock.tick(FRAMERATE)
    
pygame.quit()