import pygame

class Resolution:
    WIDTH = 1280
    HEIGHT = 720
    X_OFFSET = 0
    Y_OFFSET = 0
    SCALE = 0

class Display:
    WIDTH = 1280
    HEIGHT = 720


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
    "interact" : pygame.K_e,
    "dialogue_next" : pygame.K_SPACE
}

def set_resolution(width, height):

    rs = min(Display.WIDTH // width, Display.HEIGHT // height)

    if rs <= 0:
        print("Display too small to display target resolution")
        return

    Resolution.WIDTH = width
    Resolution.HEIGHT = height
    Resolution.SCALE = rs
    Resolution.X_OFFSET = (Display.WIDTH - Resolution.WIDTH * Resolution.SCALE) // 2
    Resolution.Y_OFFSET = (Display.HEIGHT - Resolution.HEIGHT * Resolution.SCALE) // 2

    return pygame.Surface((Resolution.WIDTH, Resolution.HEIGHT))