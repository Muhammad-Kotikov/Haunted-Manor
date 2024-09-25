import pygame

# https://www.youtube.com/watch?v=AY9MnQ4x3zk / Mua / 23.09.24
# Danke Muha / 25.09.24

# Titel wird über dem Fenster angezeigt
TITLE = "Haunted Manor"

# TILE_SIZE ist die Pixelgröße eines Feldes im Spiel
TILE_SIZE = 16

# WIDTH und HEIGHT geben an wie viele Felder in vertikel und horizontal in die Malfläche reinpassen
WIDTH = 10
HEIGHT = 10

# Jeder Pixel der Malfläche wird mit diesem Wert multipliziert, das heißt die Pixel werden vergrößert um den FaktorSCALE
SCALE = 5

# So oft läuft die Spielschleife pro Sekunde, das heißt es wird FRAMERATE oft bspw. die Kollision gecheckt,
# so viele Bilder werden angezeigt und so oft kann sich etwas auf dem Bildschirm bewegen
FRAMERATE = 30

# Berechnung der Malflächegröße (in Pixel) und der tatsächlichen Auflösung/Fenstergröße (in Pixel)
CANVAS_WIDTH = WIDTH * TILE_SIZE
CAVNAS_HEIGHT = HEIGHT * TILE_SIZE

RESOLUTION_DIMENSIONS = (CANVAS_WIDTH, CAVNAS_HEIGHT)
SCREEN_DIMENSIONS = (CANVAS_WIDTH * SCALE, CAVNAS_HEIGHT * SCALE)

# Startet irgendwelche Hintergrundgeschichten
pygame.init()

# Bildschirm und Zeichenfläche erstellen
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
canvas = pygame.Surface(RESOLUTION_DIMENSIONS)
pygame.display.set_caption(TITLE)

# TEST: Spielerbild laden
player_sprite = pygame.image.load("lia.png").convert()

# Eine Uhr erstellen, die die Geschwindigkeit, in der die Loop und somit das gesamt Spiel läuft, steuert
clock = pygame.time.Clock()
running = True

# Gameloop
while running:

    # Malfläche zurücksetzen
    canvas.fill("Black")

    # TEST: Spielerbild zeichnen
    canvas.blit(player_sprite, (0, 0))

    # Malfläche hochskalieren damit die Pixel nicht so klein sind
    # https://stackoverflow.com/questions/34910086/pygame-how-do-i-resize-a-surface-and-keep-all-objects-within-proportionate-to-t / Mua / 25.09.2024
    screen.blit(pygame.transform.scale(canvas, screen.get_rect().size), (0, 0))
    pygame.display.update()

    # Fenster schließbar machen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    clock.tick(FRAMERATE)

