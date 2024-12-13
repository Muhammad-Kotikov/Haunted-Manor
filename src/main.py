from game import *
import pygame

# einzelne funktionen müssen hier schon initialisiert werden weil sonst die Bilder nicht laden
pygame.init()
pygame.mixer.init()
pygame.display.set_mode()

m = MainMenu()
i = InGame()
d = InDialogue()

game = Game(d)
game.menu = m
game.ingame = i
game.indialogue = d

while game.running:

    game.screen.fill((0, 0, 0))
    game.update()
    game.render()
    pygame.display.update()

    game.delta = game.clock.tick(FRAMERATE)

    if game._state != game._next_state:
        game.transition_to(game._next_state)
 