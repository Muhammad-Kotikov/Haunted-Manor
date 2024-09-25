import pygame

# https://www.youtube.com/watch?v=AY9MnQ4x3zk / Mua / 23.09.24
# Danke Muha / 25.09.24

TITLE = "Haunted Manor"

TILE_SIZE = 16
WIDTH = 10
HEIGHT = 10
SCALE = 5

FRAMERATE = 30

CANVAS_WIDTH = WIDTH * TILE_SIZE
CAVNAS_HEIGHT = HEIGHT * TILE_SIZE

RESOLUTION_DIMENSIONS = (CANVAS_WIDTH, CAVNAS_HEIGHT)
SCREEN_DIMENSIONS = (CANVAS_WIDTH * SCALE, CAVNAS_HEIGHT * SCALE)

# Pygame Hintergrundzeug starten
pygame.init()

# Bildschirm erstellen und einstellen
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
canvas = pygame.Surface(RESOLUTION_DIMENSIONS)
pygame.display.set_caption(TITLE)


player_sprite = pygame.image.load("lia.png").convert()

# Eine Uhr erstellen, die die Gameloop steuert
clock = pygame.time.Clock()
running = True

# Gameloop
while running:

    # Malfläche zurücksetzen
    canvas.fill("Black")

    canvas.blit(player_sprite, (0, 0))

    # Fertig gerenderte Malfläche zur Bildschirmgröße skalieren und zeichnen
    # https://stackoverflow.com/questions/34910086/pygame-how-do-i-resize-a-surface-and-keep-all-objects-within-proportionate-to-t / Mua / 25.09.2024
    screen.blit(pygame.transform.scale(canvas, screen.get_rect().size), (0, 0))
    pygame.display.update()

    # Framerate festsetzen
    clock.tick(FRAMERATE)

    # Fenster schließbar machen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False