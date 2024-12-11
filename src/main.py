import pygame
import shader

from tools import *
from camera import *
from settings import *
from world import *
from hud import *

from entities.creatures.player import *
from entities.creatures.enemy import *
from entities.tile import *
from entities.tiles.trap import *
from entities.tiles.itile import *
from entities.tiles.door import *

# https://www.youtube.com/watch?v=AY9MnQ4x3zk / Mua / 23.09.24
# Danke Muha / 25.09.24

rect = pygame.Rect

def init():
    pygame.init()
    pygame.mixer.init()


def update(delta):

    if paused == True:
        return
    world.update(delta)
    camera.update()


def render():
    # Malfläche zurücksetzen
    screen.fill((255, 255, 255))

    world.render(screen, camera)
    camera.render(screen)

    rel_player_pos_cam = world.player.rect.center - camera.position
    shader.add_light_source(rel_player_pos_cam, 50)
    shader.lightning()
    hud.render(screen)



    # Malfläche anzeigen
    pygame.display.flip()


def start_piano():
    import puzzles.kryptex
    screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SCALED + pygame.FULLSCREEN)

running = True
paused = False
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SCALED + pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)

init()

shader.init(screen)

########################################## BESSEREN CODE ZUM LADEN VON OBJEKTEN ##########################################

sprites = {}

for sprite in ['brick', 'pumpkin', 'heart', 'empty_heart', 'piano', 'door']:
    sprites[sprite] = get_sprite(sprite + ".png")

brick = Tile(True, sprites['brick'])
piano = ITile(rect(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), start_piano, None, True, sprites['piano'])

player = Player(3, sprites['pumpkin'])
enemy = Enemy(10, get_sprite("anna.png"),15* TILE_SIZE, 5 * TILE_SIZE,16,16)
saw = Trap(CYCLING, [(0, 0, 0, 0, 120), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4, 30)], False, get_sprite("skull_trap.png"), 0, 0, TILE_SIZE, TILE_SIZE)
smart_saw = Trap(DETECTING, [(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), (0, 0, 0, 0, 1), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4, 999999)], False, get_sprite("skull_trap.png"))
door = Door(rect(-TILE_SIZE / 2, - TILE_SIZE / 2, TILE_SIZE * 2, TILE_SIZE * 2), True, sprites['door'])

spawn_table = [None, brick, player, piano, door, saw, smart_saw, enemy]

world = World(get_map("test_tilemap.tmx"), spawn_table)
camera = Camera(rect(0, 0, WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), rect(0.0, 0.0, world.width * TILE_SIZE, world.height * TILE_SIZE), player)

hud = HUD(player, sprites['heart'], sprites['empty_heart'])
##########################################################################################################################

delta = 1

while running:

    for event in pygame.event.get():

        #Fenster schließbar machen
        if event.type == pygame.QUIT:
            running = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            paused = not paused

    update(delta)
    render()
        
    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    delta = clock.tick(FRAMERATE)
    
pygame.quit()