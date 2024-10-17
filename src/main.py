import pygame
from entity.creature.player.player import Player

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
FRAMERATE = 60

running = True
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH * TILE_SIZE, HEIGHT * TILE_SIZE), pygame.SCALED)
pygame.display.set_caption(TITLE)

creatures = []

def init():
    pygame.init()
    pygame.mixer.init()
    

def update(delta_time):

    for creature in creatures:
        creature.update(delta_time)

def render():
    # Malfläche zurücksetzen
    screen.fill((0, 0, 0))

    for creature in creatures:
        creature.render(screen)

    # Malfläche anzeigen
    pygame.display.flip()


init()
player = Player()
creatures.append(player)
delta_scale = 1

while running:

    for event in pygame.event.get():

        # Fenster schließbar machen
        if event.type == pygame.QUIT:
            running = False

    update(delta_scale)
    render()

    # Warten paar Millisekunden damit das Spiel nicht unendlich schnell läuft
    delta_scale = FRAMERATE * 0.001 * clock.tick(FRAMERATE)
    
pygame.quit()