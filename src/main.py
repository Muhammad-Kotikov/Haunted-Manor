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

# So oft läuft die Spielschleife pro Sekunde, das heißt es wird FRAMERATE oft bspw. die Kollision gecheckt,
# so viele Bilder werden angezeigt und so oft kann sich etwas auf dem Bildschirm bewegen
FRAMERATE = 30

running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
pygame.display.set_caption(TITLE)

entities = []

def init():
    pygame.init()
    pygame.mixer.init()
    

def update():

    for entity in entities:
        entity.update(delta_time)

def render():
    # Malfläche zurücksetzen
    screen.fill((0, 0, 0))

    for entity in entities:
        entity.render()

    # Malfläche anzeigen
    pygame.display.flip()


init()

while running:

    for event in pygame.event.get():

        # Fenster schließbar machen
        if event.type == pygame.QUIT:
            running = False

    update()
    render()

    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    delta_time = clock.tick(FRAMERATE)
    
pygame.quit()