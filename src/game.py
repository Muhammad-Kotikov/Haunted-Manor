import pygame
import shader
import menu

from patterns import State, Context
from settings import *

from game import *
from tools import *
from camera import *
from world import *
from hud import *

from entities.creatures.player import *
from entities.creatures.enemy import *
from entities.tile import *
from entities.tiles.trap import *
from entities.tiles.itile import *
from entities.tiles.door import *


class Game(Context):

    def __init__(self, state: State):
        Context.__init__(self, state)

        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.screen  = pygame.display.set_mode((Resolution.WIDTH, Resolution.HEIGHT), pygame.SCALED + pygame.FULLSCREEN)
        self._next_state = state
        self.running = True
        self.delta = 0


    def update(self):
        self._state.update()
    

    def render(self):
        self._state.render()


class GameState(State):

    def update(self):
        pass


    def render(self):
        pass


class InGame(GameState):

    def __init__(self):
        Resolution.WIDTH = 20 * TILE_SIZE
        Resolution.HEIGHT = 15 * TILE_SIZE

        self.paused = False

        sprites = {}

        for sprite in ['brick', 'pumpkin', 'heart', 'empty_heart', 'piano', 'door']:
            sprites[sprite] = get_sprite(sprite + ".png")

        brick = Tile(True, sprites['brick'])
        piano = ITile(pygame.Rect(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), print, None, True, sprites['piano'])

        player = Player(3, sprites['pumpkin'])
        enemy = Enemy(10, get_sprite("anna.png"),15* TILE_SIZE, 5 * TILE_SIZE,16,16)
        saw = Trap(CYCLING, [(0, 0, 0, 0, 120), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4, 30)], False, get_sprite("skull_trap.png"), 0, 0, TILE_SIZE, TILE_SIZE)
        smart_saw = Trap(DETECTING, [(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), (0, 0, 0, 0, 1), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4, 999999)], False, get_sprite("skull_trap.png"))
        door = Door(pygame.Rect(-TILE_SIZE / 2, - TILE_SIZE / 2, TILE_SIZE * 2, TILE_SIZE * 2), True, sprites['door'])

        spawn_table = [None, brick, player, piano, door, saw, smart_saw, enemy]

        self.world = World(get_map("test_tilemap.tmx"), spawn_table)

        self.camera = Camera(pygame.Rect(0, 0, Resolution.WIDTH, Resolution.HEIGHT), pygame.Rect(0.0, 0.0, self.world.width * TILE_SIZE, self.world.height * TILE_SIZE), player)
        self.hud = HUD(player, sprites['heart'], sprites['empty_heart'])

        ###

    def update(self):

        for event in pygame.event.get():

            #Fenster schließbar machen
            if event.type == pygame.QUIT:
                self.context.running = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.context._next_state = self.context.menu
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.paused = not self.paused

        if self.paused == True:
            return
        
        self.world.update(self.context.delta)
        self.camera.update()
        #print(self.camera.position)


    def render(self):
        # Malfläche zurücksetzen
        self.context.screen.fill((255, 255, 255))

        self.world.render(self.context.screen, self.camera)
        self.camera.render(self.context.screen)

        rel_player_pos_cam = self.world.player.rect.center - self.camera.position
        shader.add_light_source(rel_player_pos_cam, 50)
        shader.lightning()
        self.hud.render(self.context.screen)


    def enter(self):
        self.context.paused = False
        Resolution.WIDTH = 20 * TILE_SIZE
        Resolution.HEIGHT = 15 * TILE_SIZE
        self.context.screen = pygame.display.set_mode((Resolution.WIDTH, Resolution.HEIGHT), pygame.SCALED + pygame.FULLSCREEN)
        shader.init(self.context.screen)
    

    def exit(self):
        self.context.paused = True


class MainMenu(GameState):

    def __init__(self):
        Resolution.WIDTH = 1200
        Resolution.HEIGHT = 800
        self.menu = menu.Menu()

    
    def update(self):

        self.menu.update()

        if self.menu.start:
            self.context._next_state = self.context.ingame
        elif self.menu.exit:
            self.context.running = False


    def render(self):
        self.menu.render()


    def enter(self):
        Resolution.WIDTH = 1200
        Resolution.HEIGHT = 800
        
        self.context.screen = pygame.display.set_mode((Resolution.WIDTH, Resolution.HEIGHT), pygame.SCALED + pygame.FULLSCREEN)
        self.menu.screen = self.context.screen

        self.menu.start = False
        self.menu.main_menu = True
