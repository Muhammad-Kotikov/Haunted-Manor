from pygame import Surface, surfarray, Vector2
import numpy as np

s = None
h = 0
w = 0

light_map = None
ambient_light = 0.15

def init(screen : Surface):

    global s
    global w
    global h
    global light_map

    s = screen
    h = screen.get_height()
    w = screen.get_width()
    light_map = np.zeros(shape=(w, h)).astype(np.float16)

# Mit Hilfe von ChatGPT, allerdings stark überarbeitet
def lightning():
    
    # Pixel (Refferenzen) holen
    # 3D = 3 Dimensionen (Breite, Höhe, Farbkanal [Rot, Grün, Blau])
    # 3D > 2D weil 2D müssen wir Dec Farbwerte -> Hex Farbwerte
    p = surfarray.pixels3d(s)

    # Farben trennen
    r = p[:, :, 0]
    g = p[:, :, 1]
    b = p[:, :, 2]

    ### Farben dunkel färben (numpy magie)
    r = (r * light_map).astype(np.uint8)
    g = (g * light_map).astype(np.uint8)
    b = (b * light_map * 0.9).astype(np.uint8)

    # Array mit neuen Farben updaten
    p[:, :, 0] = r
    p[:, :, 1] = g
    p[:, :, 2] = b


def add_light_source(point : Vector2, radius : int):

    # https://stackoverflow.com/questions/61628380/calculate-distance-from-all-points-in-numpy-array-to-a-single-point-on-the-basis
    def dist_map(a, index):
        i,j = np.indices(a.shape, sparse=True)
        return np.sqrt((i-index[0])**2 + (j-index[1])**2)

    point_array = [point.x, point.y]

    # Grenzen der Lichtberechnung zur Optimierung
    min_x = int(max(0, point.x - radius))
    max_x = int(min(point.x + radius, w))
    min_y = int(max(0, point.y - radius))
    max_y = int(min(point.y + radius, h))
    

    global light_map

    # leeres array erstellen (ds = distance-shadow ...
    # because its the distance and shadow and whatever)
    ds = np.zeros(light_map.shape)
    # distanzen berechnen (danke stack overflow)
    ds = dist_map(ds, point_array)
    # (relevanten) werte auf 0.0 - 1.0 skalieren
    # (manche sind über 1.0, werden nächste zeile gefiltert)
    ds = ds / radius
    # licht beschränken
    ds = np.clip(ds, a_min=0, a_max=1 - ambient_light)
    # invertieren (kleinere distanz = hellere farbe)
    light_map = 1.0 - ds


def get_light_map():

    return light_map