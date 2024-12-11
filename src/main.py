from game import *
import pygame

# einzelne funktionen müssen hier schon initialisiert werden weil sonst die Bilder nicht laden
pygame.init()
pygame.mixer.init()
pygame.display.set_mode()

m = MainMenu()
i = InGame()

game = Game(m)
game.menu = m
game.ingame = i

while game.running:

    game.update()
    game.render()
    pygame.display.update()

    game.delta = game.clock.tick(FRAMERATE)

    if game._state != game._next_state:
        game.transition_to(game._next_state)

quit()