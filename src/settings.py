import pygame

class Resolution:
    WIDTH = 1200
    HEIGHT = 800

# Titel wird über dem Fenster angezeigt
TITLE = "Haunted Manor"

# TILE_SIZE ist die Pixelgröße eines Feldes im Spiel
TILE_SIZE = 16

# So oft läuft die Spielschleife pro Sekunde, das heißt es wird FRAMERATE oft bspw. die Kollision gecheckt,
# so viele Bilder werden angezeigt und so oft kann sich etwas auf dem Bildschirm bewegen
FRAMERATE = 60

# Debug
DEBUGGING = False
SHOW_COLLISION_RANGE = True
SHOW_MOVEMENT_VECTORS = True

# Keymapping
key_map = {
    "left" : pygame.K_a,
    "right" : pygame.K_d,
    "up" : pygame.K_w,
    "down" : pygame.K_s,
    "interact" : pygame.K_e
}
