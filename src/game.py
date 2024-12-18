import pygame
import shader
import menu
import dialogue

import kryptex
import clock
import memory
import piano

from patterns import State, Context
from settings import *

from game import *
from tools import *
from camera import *
from world import *
from hud import *
from pausemenu import *
from intro import *

from entities.creatures.player import *
from entities.creatures.enemy import *
from entities.tile import *
from entities.tiles.trap import *
from entities.tiles.itile import *
from entities.tiles.door import *
from entities.powerup import *
class Game(Context):

    def __init__(self, state: State):
        Context.__init__(self, state)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
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
        _ = set_resolution(16 * TILE_SIZE, 9 * TILE_SIZE)

        self.paused = False
        self.timer = FRAMERATE * 3
        self.final_key = False
        self.won = False

        sprites = {}
        for sprite in ['brick', 'heart', 'empty_heart', 'piano', 'kryptex', 'memory', 'clock', 'powerup_heal', 'powerup_speed', 'powerup_nightvision',
                       'notes', 'door', 'bloody_door', 'bloody_brick', 'penta', 'quake', 'floor_0', 'floor_1']:
            sprites[sprite] = get_sprite(sprite + ".png")

        # player
        player = Player(4, get_sprite("player_idle_0.png"), width = 14, height = 14)
        enemy = Enemy(4, get_sprite("enemy.png"), width = 14, height = 14)


        # puzzle tiles
        def start_kryptex():
            self.context._next_state = self.context.inkryptex

        def start_clock():
            self.context._next_state = self.context.inclock

        def start_memory():
            self.context._next_state = self.context.inmemory
        
        def start_piano():
            self.context._next_state = self.context.inpiano

        def show_dialogue(puzzle):

            if puzzle == 'piano':
                txt = ["pi" * 4, "pa" * 5]
                bgs = [get_sprite(f"dialogue_{i}.png") for i in range(2)]
            elif puzzle == 'memory':
                txt = ["me" * 4, "mo" * 5]
                bgs = [get_sprite(f"dialogue_{i}.png") for i in range(2)]
            elif puzzle == 'kryptex':
                txt = ["kry" * 4, "tex" * 5]
                bgs = [get_sprite(f"dialogue_{i}.png") for i in range(2)]
            elif puzzle == 'clock':
                txt = ["clo" * 4, "ock" * 5]
                bgs = [get_sprite(f"dialogue_{i}.png") for i in range(2)]
            else:
                return

            self.context._next_state = InDialogue(txt, bgs)

        piano = ITile(pygame.Rect(-8, -8, 32, 32), start_piano , None, False, sprites['piano'])
        memory = ITile(pygame.Rect(-8, -8, 32, 32), start_memory , None, False, sprites['memory'])
        kryptex = ITile(pygame.Rect(-8, -8, 32, 32), start_kryptex , None, False, sprites['kryptex'])
        clock = ITile(pygame.Rect(-8, -8, 32, 32), start_clock , None, False, sprites['clock'])

        notes_piano = ITile(pygame.Rect(-8, -8, 32, 32), show_dialogue, 'piano', False, sprites['notes'])
        notes_memory = ITile(pygame.Rect(-8, -8, 32, 32), show_dialogue, 'memory', False, sprites['notes'])
        notes_kryptex = ITile(pygame.Rect(-8, -8, 32, 32), show_dialogue, 'kryptex', False, sprites['notes'])
        notes_clock = ITile(pygame.Rect(-8, -8, 32, 32), show_dialogue, 'clock', False, sprites['notes'])

        # static tiles
        brick = Tile(True, sprites['brick'])
        floor_0 = Tile(False, sprites['floor_0'])
        floor_1 = Tile(False, sprites['floor_1'])
        
        bloody_brick = Tile(True, sprites['bloody_brick'])
        penta = Tile(False, sprites['penta'])
        quake = Tile(False, sprites['quake'])

        # door tiles
        door = Door(pygame.Rect(-TILE_SIZE, - TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), True, sprites['door'])

        def game_won():

            if self.world.player.key_final:
                self.context._next_state = InDialogue(['You\'re free..........................', "..."], [get_sprite("free_0.png"), get_sprite("free_0.png")])
                self.won = True
            else:
                self.context._next_state = InDialogue(["You dream of freedom"], [get_sprite("closed.png")])


        # game over tile
        bloody_door = ITile(pygame.Rect(-8, -8, 32, 32), game_won, None, True, sprites['bloody_door'])

        # trap tiles
        spikes = Trap(DETECTING, [(0, 0, 16, 16), (0, 0, 0, 0, 1), (0, 0, 0, 0, 30), (2, 2, 12, 12, 9999999)], False, get_sprite("spike_0.png"))
        spikes.sprites = {} # quick and dirty
        for i, sprite in enumerate([f'spike_{i}' for i in range(3)]):
            spikes.sprites[i] = get_sprite(sprite + ".png")

        fire_trap = Trap(CYCLING, [(0, 0, 0, 0, 30), (0, 0, 0, 0, 15), (1, 3, 10, 12, 5), (1, 3, 10, 12, 5), (1, 3, 10, 12, 5), (1, 3, 10, 12, 5), (1, 3, 10, 12, 5)], False, get_sprite("fire_trap_0.png"))
        fire_trap.sprites = {} # quick and dirty
        for i, sprite in enumerate([f'fire_trap_{i}' for i in range(7)]):
            fire_trap.sprites[i] = get_sprite(sprite + ".png")

        # powerups
        def heal():
            self.world.player.health = min(self.world.player.health + 1, self.world.player.hitpoints)
        
        def speed():
            self.world.player.speed_boost_duration = FRAMERATE * 5

        def night_vision():
            shader.nv_duration = FRAMERATE * 5
        
        powerup_heal = Powerup(Rect(0, 0, TILE_SIZE, TILE_SIZE), heal, FRAMERATE * 2, sprite=sprites["powerup_heal"])
        powerup_speed = Powerup(Rect(0, 0, TILE_SIZE, TILE_SIZE), speed, FRAMERATE * 2, sprite=sprites["powerup_speed"])
        powerup_nightvision = Powerup(Rect(0, 0, TILE_SIZE, TILE_SIZE), night_vision, FRAMERATE * 2, sprite=sprites["powerup_nightvision"])

        
        #torch = Tile(False, sprites["torch"])

        # world
        spawn_table = [None, brick, player, piano, memory, kryptex, clock, spikes, fire_trap, powerup_heal, powerup_speed, powerup_nightvision,
                       notes_piano, notes_memory, notes_kryptex, notes_clock, bloody_brick, door, bloody_door, enemy, penta, quake, floor_0, floor_1]
        self.world = World(get_map("manor.tmx"), spawn_table)

        # misc
        self.camera = Camera(pygame.Rect(0, 0, Resolution.WIDTH, Resolution.HEIGHT), pygame.Rect(0.0, 0.0, self.world.width * TILE_SIZE, self.world.height * TILE_SIZE), player)
        self.hud = HUD(player, sprites['heart'], sprites['empty_heart'])

        shader.LightSource(player.position, vec(player.rect.width // 2, player.rect.height // 2), 100, (175, 125, 125)) # quick and dirty

    def update(self):



        if  self.won:
            m = InMenu()
            m.resetgame = True
            self.context._next_state = m
            return
        
        elif not self.world.player:                                                              #wird ausgeführt wenn es keinen Spieler in  der Welt gibt, also gestorben ist               
            m = InMenu()                                                                         # bringt den Spieler zurück ins Menü
            m.resetgame = True                                                                   #resettet das Game
            d = InDialogue(['YOU DIED'],[get_sprite("enemy.png")], m)                            #Zeigt einen Dialog an und ein Bild
            self.context._next_state = d                                                         #Zustand vom Spiel wird geändert
            return
            

        elif self.world.player.keys >= 3 and not self.world.player.key_final:
            
            if self.timer > 0:
                self.timer -= 1

            elif self.timer <= 0:
                self.world.player.key_final = True
                self.context._next_state = InDialogue(['The key fragments violently merge into one.\n\n\n\n\nYou feel a sense of relief.'], [get_sprite("key_final.png")])
                return

        for event in pygame.event.get():

            #Fenster schließbar machen
            if event.type == pygame.QUIT:
                self.context.running = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.context._next_state = self.context.inmenu
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.paused = not self.paused

        if self.paused == True:
            return
        
        self.world.update(self.context.delta)
        self.camera.update()


    def render(self):
        self.context.screen.fill((0, 0, 0))
        self.world.render(self.context.screen, self.camera)
        self.camera.render(self.context.screen)
        shader.lightning()
        self.hud.render(self.context.screen)
        shader.crt()


    def enter(self):
        self.context.paused = False
        self.context.screen = set_resolution(16 * TILE_SIZE, 9 * TILE_SIZE)
        shader.init(self.context.screen, self.camera)


    def exit(self):
        self.context.paused = True



class InMenu(GameState):

    def __init__(self):
        _ = set_resolution(1200, 800)
        self.menu = menu.Menu()
        self.resetgame = False

    
    def update(self):

        self.menu.update()

        if self.menu.start:
            self.context._next_state = self.context.ingame
        elif self.menu.exit:
            self.context.running = False


    def render(self):
        self.menu.render()


    def enter(self):

        if self.resetgame:
            self.context.ingame = InGame()

        self.context.screen = set_resolution(1200, 800)
        self.menu.screen = self.context.screen

        self.menu.start = False
        self.menu.main_menu = True

    def exit(self):
        for button in self.menu.buttons:
            button['clicked'] = False


class InDialogue(GameState):

    def __init__(self, txt, bgs,next_state=None):
        _ = set_resolution(400, 400)
        self.next_state = next_state

        #self.dialogue.screen = pygame.Surface((400, 400))

        self.dialogue = dialogue.Dialogue(txt, bgs)

    def update(self):
        self.dialogue.update()
        if not self.dialogue.done:
            return
        elif self.next_state is None:
            self.context._next_state = self.context.ingame
        else:
            self.context._next_state = self.next_state
        


    def render(self):
        self.dialogue.render()


    def enter(self):
        self.context.screen = set_resolution(400, 400)
        self.dialogue.screen = self.context.screen

        self.dialogue.exit = False
        self.dialogue.phase = 0


    def exit(self):
        self.dialogue.phase = 0
        self.dialogue.text_amount = 0
        self.dialogue.text_frame = 0
        self.dialogue.done = False

class InKryptex(GameState):

    def __init__(self):
        _ = set_resolution(1000, 800)
        self.rewarded = False

        self.puzzle = kryptex.Kryptex()

    
    def update(self):
        self.puzzle.update()
        if self.puzzle.exit:
            self.context._next_state = self.context.ingame


    def render(self):
        self.puzzle.render()

    
    def enter(self):
        self.context.screen = set_resolution(1000, 800)
        self.puzzle.screen = self.context.screen


    def exit(self):
        if self.puzzle.won and not self.rewarded:
            self.context.ingame.world.player.keys += 1
            self.rewarded = True
            self.context.ingame.world.interactables.remove(self.context.ingame.world.player.interactables[0])
            self.context._next_state = InDialogue(['You\'ve finished the puzzle, the computer disappears in front of your eyes.\n' +
                                                   'After a blinding blood red flash a sharp object materializes in front of you.\n\n' +
                                                   'It\'s a key fragment. You have no use for this yet...'],
                                                   [get_sprite("key_appear.png")])


class InClock(GameState):

    def __init__(self):
        _ = set_resolution(800, 800)
        self.rewarded = False
        self.puzzle = clock.Clock()

    
    def update(self):
        self.puzzle.update()
        if self.puzzle.exit:
            self.context._next_state = self.context.ingame


    def render(self):
        self.puzzle.render()

    
    def enter(self):
        self.context.screen = set_resolution(800, 800)
        self.puzzle.screen = self.context.screen


    def exit(self):
        if self.puzzle.won and not self.rewarded:
            self.context.ingame.world.player.keys += 1
            self.rewarded = True
            self.context.ingame.world.interactables.remove(self.context.ingame.world.player.interactables[0])
            self.context._next_state = InDialogue(['You\'ve finished the puzzle, the clock disappears in front of your eyes.\n' +
                                                   'After a blinding blood red flash a sharp object materializes in front of you.\n\n' +
                                                   'It\'s a key fragment. You have no use for this yet...'],
                                                   [get_sprite("key_appear.png")])


class InMemory(GameState):

    def __init__(self):
        _ = set_resolution(800, 875)
        self.rewarded = False
        self.puzzle = memory.Memory()

    
    def update(self):
        self.puzzle.update()
        if self.puzzle.exit:
            self.context._next_state = self.context.ingame


    def render(self):
        self.puzzle.render()

    
    def enter(self):
        self.context.screen = set_resolution(800, 875)
        self.puzzle.screen = self.context.screen
        self.puzzle.enter()
        self.puzzle.start_time      = pygame.time.get_ticks()


    def exit(self):
        if self.puzzle.won and not self.rewarded:
            self.context.ingame.world.player.keys += 1
            self.rewarded = True
            self.context.ingame.world.interactables.remove(self.context.ingame.world.player.interactables[0])
            self.context._next_state = InDialogue(['You\'ve finished the puzzle, the cards disappears in front of your eyes.\n' +
                                                   'After a blinding blood red flash a sharp object materializes in front of you.\n\n' +
                                                   'It\'s a key fragment. You have no use for this yet...'],
                                                   [get_sprite("key_appear.png")])
        if self.puzzle.lost:
            self.puzzle.reset()


class InPiano(GameState):

    def __init__(self):
        _ = set_resolution(52 * 25, 800)
        self.puzzle = piano.Piano()

    
    def update(self):
        if self.puzzle.exit:
            self.context._next_state = self.context.ingame
        self.puzzle.update()


    def render(self):
        self.puzzle.render()

    
    def enter(self):
        self.context.screen = _ = set_resolution(52 * 25, 800)
        self.puzzle.screen = self.context.screen
        self.puzzle.exit = False


    def exit(self):
        pass


class InPause(GameState):
    def __init__(self):
        _ = set_resolution(400, 400)
        self.pausemenu = PauseMenu()

    def update(self):
        if not self.pausemenu.paused:
            self.context._next_state = self.context.ingame
        self.pausemenu.update_pausemenu()

    def render(self):
        self.pausemenu.render_pause_screen()

    def enter(self):
        self.context.screen = set_resolution(400, 400)
        self.pausemenu.screen = self.context.screen

    def exit(self):
        self.pausemenu.done = False

class InIntro(GameState):
    def __init__(self):
        _ = set_resolution(400, 400)
        self.intro = Intro()

    def update(self):
        if not self.intro.running:
            self.context._next_state = self.context.menu

    def render(self):
        self.intro.render_intro()

    def enter(self):
        self.context.screen = set_resolution(400, 400)

    def exit(self):
        self.intro.done = True
