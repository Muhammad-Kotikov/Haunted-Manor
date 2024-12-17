from game import *
import pygame
from settings import Display, Resolution

# einzelne funktionen müssen hier schon initialisiert werden weil sonst die Bilder nicht laden
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(50)
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

display_info = pygame.display.Info()
Display.WIDTH = display_info.current_w
Display.HEIGHT = display_info.current_h

display = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT), pygame.FULLSCREEN)

game = Game(InMenu())
game.inmenu = InMenu()
game.ingame = InGame()
game.inkryptex = InKryptex()
game.inclock = InClock()
game.inmemory = InMemory()
game.inpiano = InPiano()
game.inpause= InPause()
game.inintro= InIntro()

game.transition_to(game.inmenu)

while game.running:

    display.fill((0, 0, 0))
    game.update()
    game.render()
    display.blit(pygame.transform.scale_by(game.screen, Resolution.SCALE), (Resolution.X_OFFSET, Resolution.Y_OFFSET))
    pygame.display.update()

    game.delta = game.clock.tick(FRAMERATE)

    if game._state != game._next_state:
        game.transition_to(game._next_state)
 