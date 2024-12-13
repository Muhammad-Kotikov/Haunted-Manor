import pygame
import shader
import menu
import dialogue

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
from entities.powerup import *
class Game(Context):

    def __init__(self, state: State):
        Context.__init__(self, state)

        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        #self.screen = set_resolution(Display.WIDTH, Display.HEIGHT)
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

        sprites = {}

        for sprite in ['brick', 'pumpkin', 'heart', 'empty_heart', 'piano', 'door', 'torch', 'health_pickup', 'speed_pickup', 'nv_pickup']:
            sprites[sprite] = get_sprite(sprite + ".png")

        brick = Tile(True, sprites['brick'])
        piano = ITile(pygame.Rect(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), print, None, True, sprites['piano'])

        player = Player(3, sprites['pumpkin'])
        enemy = Enemy(10, get_sprite("anna.png"),15* TILE_SIZE, 5 * TILE_SIZE,16,16)
        saw = Trap(CYCLING, [(0, 0, 0, 0, 120), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4, 30)], False, get_sprite("skull_trap.png"))
        smart_saw = Trap(DETECTING, [(-TILE_SIZE, -TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), (0, 0, 0, 0, 1), (2, 2, TILE_SIZE - 4, TILE_SIZE - 4, 999999)], False, get_sprite("skull_trap.png"))
        door = Door(pygame.Rect(-TILE_SIZE, - TILE_SIZE, TILE_SIZE * 3, TILE_SIZE * 3), True, sprites['door'])
        torch = Tile(False, sprites["torch"])


        def heal():
            self.world.player.health = min(self.world.player.health + 1, self.world.player.hitpoints)
        
        def speed():
            self.world.player.speed_boost_duration = 60 * 5

        def night_vision():
            shader.nv_duration = 60 * 5

        health_pickup = Powerup(Rect(0, 0, TILE_SIZE, TILE_SIZE), heal, sprite=sprites["health_pickup"])
        speed_pickup = Powerup(Rect(0, 0, TILE_SIZE, TILE_SIZE), speed, sprite=sprites["speed_pickup"])
        nv_pickup = Powerup(Rect(0, 0, TILE_SIZE, TILE_SIZE), night_vision, sprite=sprites["nv_pickup"])

        spawn_table = [None, brick, player, piano, door, saw, smart_saw, enemy, torch, health_pickup, speed_pickup, nv_pickup]

        self.world = World(get_map("test_tilemap.tmx"), spawn_table)

        self.camera = Camera(pygame.Rect(0, 0, Resolution.WIDTH, Resolution.HEIGHT), pygame.Rect(0.0, 0.0, self.world.width * TILE_SIZE, self.world.height * TILE_SIZE), player)
        self.hud = HUD(player, sprites['heart'], sprites['empty_heart'])

        shader.LightSource(player.position, vec(player.rect.width // 2, player.rect.height // 2), 100, (175, 125, 125))
        ###

    def update(self):

        for event in pygame.event.get():

            #Fenster schließbar machen
            if event.type == pygame.QUIT:
                self.context.running = False
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.context._next_state = self.context.indialogue
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
        shader.lightning()
        self.hud.render(self.context.screen)
        shader.crt()


    def enter(self):
        self.context.paused = False
        self.context.screen = set_resolution(16 * TILE_SIZE, 9 * TILE_SIZE)
        shader.init(self.context.screen, self.camera)
    

    def exit(self):
        self.context.paused = True


class MainMenu(GameState):

    def __init__(self):
        self.screen = set_resolution(1200, 800)
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

        self.context.screen = set_resolution(1200, 800)
        self.menu.screen = self.context.screen

        self.menu.start = False
        self.menu.main_menu = True


class InDialogue(GameState):

    def __init__(self):
        _ = set_resolution(400, 400)
        #self.dialogue.screen = pygame.Surface((400, 400))

        bgs = [get_sprite(f"dialogue_{i}.png") for i in range(2)]
        txt = ["ha" * 50, "have fun" * 5]

        self.dialogue = dialogue.Dialogue(txt, bgs)

    def update(self):
        self.dialogue.update()
        if self.dialogue.done:
            self.context._next_state = self.context.ingame


    def render(self):
        self.dialogue.render()
        pass


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

class INPause(GameState):
    def __init__(self):
        _ = set_resolution(400, 400)

    def update(self):
        pass


    def render(self):
        pass


    def enter(self):
        self.context.screen = set_resolution(400, 400)

    def exit(self):
        pass

class InIntro(GameState):
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Intro Video")
        self.video = None
        self.clock = pygame.time.Clock()

        self.video = VideoFileClip("path_to_your_video.mp4")
        self.video.preview()

    def update(self):
        pass

    def render(self):
        if self.video:
            frame = self.video.get_frame(self.clock.get_time() / 1000.0)
            frame_surface = pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB")
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FRAMERATE) 

    def enter(self):
        # Lade das Video
        pass

    def exit(self):
        self.video.close()
        pygame.quit()
