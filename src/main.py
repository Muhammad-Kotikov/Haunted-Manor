from game import *
import pygame
from settings import Display, Resolution

# einzelne funktionen müssen hier schon initialisiert werden weil sonst die Bilder nicht laden
pygame.init()
pygame.mixer.init()
pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

display_info = pygame.display.Info()
Display.WIDTH = display_info.current_w
Display.HEIGHT = display_info.current_h

display = pygame.display.set_mode((Display.WIDTH, Display.HEIGHT), pygame.FULLSCREEN)

i = InGame()
k = InKryptex()
o = InClock()
m = InMemory()
p = InPiano()

game = Game(MainMenu())
game.ingame = i
game.inkryptex = k
game.inclock = o
game.inmemory = m
game.inpiano = p
  
while game.running:

    display.fill((0, 0, 0))
    game.update()
    game.render()
    display.blit(pygame.transform.scale_by(game.screen, Resolution.SCALE), (Resolution.X_OFFSET, Resolution.Y_OFFSET))
    pygame.display.update()

    game.delta = game.clock.tick(FRAMERATE)

    if game._state != game._next_state:
        game.transition_to(game._next_state)
 