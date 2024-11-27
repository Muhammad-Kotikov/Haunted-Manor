import pygame
import os

from camera import Camera
from settings import *
from entity.creature.player.player import *
from world import World
from entity.tile.tile import Tile
from entity.tile.trap.trap import *
from hud import *

# https://www.youtube.com/watch?v=AY9MnQ4x3zk / Mua / 23.09.24
# Danke Muha / 25.09.24

def init():
    pygame.init()
    pygame.mixer.init()


def get_game_folder():
    """
    Returns the Gamefolder
    """
    # os.path.dirname() is weird
    return os.path.dirname(os.path.dirname(__file__))


def get_sprite(filename: str):

    try:
        # das ".convert" sorgTilet für bessere Performanz laut Tutorial und Pygame docs
        # muss man nicht verstehen xD, ".convert_alpha für Bilder mit Alpha Kanal (Tranzparenz für normal Sterbliche)
        sprite = pygame.image.load(os.path.join(get_game_folder(), f'rsc/sprites/{filename}')).convert_alpha()
        return sprite
            
    except:
        print("ERROR Loading sprite", filename)


def get_map(filename: str):

    try:
        return open(os.path.join(get_game_folder(), f'rsc/maps/{filename}'), "rt")
    
    except:
        print("ERROR: Loading map ", filename)


def update(delta):
    camera.update()
    world.update(delta)


def render():
    # Malfläche zurücksetzen
    screen.fill((0, 0, 0))

    world.render(screen, camera)
    camera.render(screen)

    hud.render(screen)

    # Malfläche anzeigen
    pygame.display.flip()

running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SCALED + pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)

init()

brick = Tile(True, get_sprite("brick.png"), 0, 0, 16, 16)

player = Player(3, get_sprite("pumpkin.png"), 0, 0, TILE_SIZE, TILE_SIZE)
saw = Trap(CYCLING, [(0, 0, 0, 0, 120), (0, 0, TILE_SIZE - 8, TILE_SIZE - 8, 30), (8, 8, TILE_SIZE - 8, TILE_SIZE - 8, 30)], False, get_sprite("skull_trap.png"), 0, 0, TILE_SIZE, TILE_SIZE)
spawn_table = [None, brick, player, saw]

world = World(get_map("test_tilemap.tmx"), spawn_table)
camera = Camera(pygame.Rect(0, 0, WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.Rect(0.0, 0.0, world.width * TILE_SIZE, world.height * TILE_SIZE), player)

hud = HUD(player, get_sprite("heart.png"), get_sprite("empty_heart.png"))
delta = 1

while running:

    for event in pygame.event.get():

        #Fenster schließbar machen
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    update(delta)
    render()
        
    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    delta = clock.tick(FRAMERATE)
    
pygame.quit()