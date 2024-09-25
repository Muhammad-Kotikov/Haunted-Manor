import pygame

# https://www.youtube.com/watch?v=AY9MnQ4x3zk / Mua / 23.09.24
# Danke Muha / 25.09.24

# Titel wird über dem Fenster angezeigt
TITLE = "Haunted Manor"

# TILE_SIZE ist die Pixelgröße eines Feldes im Spiel
TILE_SIZE = 16

# WIDTH und HEIGHT geben an wie viele Felder in vertikel und horizontal in den Bildschirm reinpassen
WIDTH = 20
HEIGHT = 15
SCREEN_DIMENSIONS = (WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE)

# So oft läuft die Spielschleife pro Sekunde, das heißt es wird FRAMERATE oft bspw. die Kollision gecheckt,
# so viele Bilder werden angezeigt und so oft kann sich etwas auf dem Bildschirm bewegen
FRAMERATE = 30

# Startet irgendwelche Hintergrundgeschichten
pygame.init()

# Bildschirm erstellen
screen = pygame.display.set_mode(SCREEN_DIMENSIONS)
pygame.display.set_caption(TITLE)

# TEST: Spielerbild laden (das ".convert" sorgt für bessere Performanz laut Tutorial und Pygame docs
# muss man nicht verstehen xD)
player_sprite = pygame.image.load("lia.png").convert()

# Eine Uhr erstellen, die die Geschwindigkeit, in der die Loop und somit das gesamt Spiel läuft, steuert
clock = pygame.time.Clock()
running = True

# Gameloop
while running:

    ### EINGABE ###

    # Fenster schließbar machen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ### SPIELLOGIK ###


    ### SPIELGRAFIK ###

    # Malfläche zurücksetzen
    screen.fill("Black")

    # TEST: Spielerbild zeichnen
    screen.blit(player_sprite, (0, 0))

    # Malfläche hochskalieren (damit das Spiel nicht so klein ist) und anschließend anzeigen
    pygame.display.update()

    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    clock.tick(FRAMERATE)
    
pygame.quit()