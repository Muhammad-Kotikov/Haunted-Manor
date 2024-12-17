import pygame
import random

# Pygame-Initialisierung
pygame.init()

tile_size = 115  # Jedes Puzzleteil ist 115x115 Pixel groß , legt als die Teilgröße fest 
cols, rows = 3, 3  # 3x3 Puzzle-Raster (9 Teile insgesamt) wie viel halt in einer Reihe und Spalte sind 
X, Y = tile_size * cols, tile_size * rows  # Fenstergröße auf Basis der Anzahl der Puzzleteile
screen = pygame.display.set_mode((X, Y))  #erstellt ein Fenster mit der angegebenen Größe.
pygame.display.set_caption("geheimes Gemälde") # Name von dem Fenster 

# Bild laden und Puzzleteileinstellungen
image = pygame.image.load("rsc/sprites/Krauss.jpeg").convert() #für L: realtiven Pfad aus dem Sprite folder kopieren und dann einfügen
image = pygame.transform.scale(image, (X, Y))  # Das ist damit das Bild auf die Größe des Rasters angepasst wird 


tiles = [] #eine leere Liste damit die Puzzleteile darin gespeichert werden können
for y in range(rows): # teilt das Bild in einzelne Teile und speichert diese als einzelne Puzzleteile (also die Schleife)
    for x in range(cols):
        rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size) #definiert ein Rechteck, das den Bereich des Bildes umrahmt, der zu einem einzelnen Puzzleteil wird.
        tile_image = image.subsurface(rect).copy() #kopiert diesen Bildbereich als Puzzleteil.
        tile_rect = rect.copy() #kopiert das Rechteck als Platzhalter für die Position des Puzzleteils.
        tile_rect.topleft = (random.randint(0, X - tile_size), random.randint(0, Y - tile_size))  # Random Startposition der Puzzleteile
        tiles.append([tile_image, tile_rect, (x * tile_size, y * tile_size)])  # Füge Zielposition hinzu

# Variablen für das Bewegen der Puzzleteile
selected_tile = None # ist dafür da das aktuelle Puzzleteil zu speichern
offset_x, offset_y = 0, 0  # sind die Abstände zwischen Mausposition und Puzzleteil, damit es korrekt gezogen werden kann.
correctly_placed = [False] * len(tiles)  # Speichert, ob jedes Teil bereits an der richtigen Stelle ist

# Haupt-Spielschleife , erklärt sich glaube ich von selbst
game_active = True 
while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_active = False

# mit Hilfe von Chat GPT (am 08.11.2024)
        # Überprüfen, ob ein Puzzleteil ausgewählt wurde  
        elif event.type == pygame.MOUSEBUTTONDOWN: # prüft ob die linke Maustaste gedrückt wurde 
            mouse_x, mouse_y = event.pos # speichert die aktuelle Mausposition
            for index, (tile_image, rect, target_pos) in enumerate(tiles): # Schleife durchsucht alle Teile um das Angeklickte zu finden
                if not correctly_placed[index] and rect.collidepoint(mouse_x, mouse_y): #prüft, ob das Teil nicht bereits platziert ist und ob die Mausposition im Teil liegt
                    selected_tile = index #speichert den Index des ausgewählten Teils.
                    offset_x = rect.x - mouse_x 
                    offset_y = rect.y - mouse_y
                    break

        # Bewegt das ausgewählte Puzzleteil mit der Maus
        elif event.type == pygame.MOUSEMOTION and selected_tile is not None:
            mouse_x, mouse_y = event.pos
            rect = tiles[selected_tile][1]
            rect.x = mouse_x + offset_x
            rect.y = mouse_y + offset_y
# bis hier 
        # Überprüft, ob das Teil in die Nähe des Zielorts gezogen wurde und lässt es einrasten
        elif event.type == pygame.MOUSEBUTTONUP and selected_tile is not None:
            rect = tiles[selected_tile][1]
            target_x, target_y = tiles[selected_tile][2]

            # Wenn das Teil nah genug an der Zielposition ist, wird es eingerastet
            if abs(rect.x - target_x) < 30 and abs(rect.y - target_y) < 30:
                rect.topleft = (target_x, target_y)
                correctly_placed[selected_tile] = True  # Markiert das Teil als richtig platziert

            # Auswahl zurücksetzen
            selected_tile = None

    # Bildschirm leeren
    screen.fill((255, 255, 255))  # Damit wird der weiße Hintergrund erstellt, kann man aber auch beliebig ändern  

    # Puzzleteile zeichnen
    for tile_image, rect, _ in tiles:
        screen.blit(tile_image, rect.topleft)

    # Bildschirm aktualisieren
    pygame.display.flip()

# Pygame beenden
pygame.quit()


# zählen bis 9 um eine Gewinnnachricht auszugeben 