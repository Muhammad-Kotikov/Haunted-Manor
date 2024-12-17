from pygame import Surface, surfarray, Vector2
import numpy as np

s = None
r = None
g = None
b = None
h = 0
w = 0

RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2

COLOR_CHANNELS = [RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL]

light_map = None
ambient_color = None
light_sources = []

nv_duration = 0

class LightSource():

    def __init__(self, position : Vector2, offset : Vector2, radius : int, color : tuple):

        self.position = position
        self.radius = radius
        self.color = color
        self.offset = offset
        self.distance = 0
        light_sources.append(self)


    def update(self, radius = None, color = None):

        self.x = round(self.position.x - camera.position.x + self.offset.x)
        self.y = round(self.position.y - camera.position.y + self.offset.y)

        self.distance = Vector2(self.position.x - camera.rect.centerx + self.offset.x, self.position.y - camera.rect.centery + self.offset.y).length()

        if radius != None:
            self.radius = radius
        
        if color != None:
            self.color = color


def init(screen : Surface, c, a = (25, 10, 10)):

    global camera
    global s, p
    global w, h
    global light_map
    global r, g, b
    global ambient_color

    camera = c
    ambient_color = a

    s = screen
    h = screen.get_height()
    w = screen.get_width()

    light_map = np.zeros(shape=(w, h, 3)).astype(np.uint8)


def lightning():

    global nv_duration

    if nv_duration > 0:
        ac = (200, 200, 200)
    else:
        ac = ambient_color

    # Pixel (Refferenzen) holen
    # 3D = 3 Dimensionen (Breite, Höhe, Farbkanal [Rot, Grün, Blau])
    # 3D > 2D weil 2D müssen wir Dec Farbwerte -> Hex Farbwerte
    p = surfarray.pixels3d(s)
    reset(ac)
    apply_light_sources()
    apply_light_map(p)
    nv_duration -= 1


# Mit Hilfe von ChatGPT, allerdings stark überarbeitet
def reset(ac = ambient_color):

    for channel in COLOR_CHANNELS:
        light_map[:, :, channel] = ac[channel]


def apply_light_sources():

    
    # https://stackoverflow.com/questions/61628380/calculate-distance-from-all-points-in-numpy-array-to-a-single-point-on-the-basis
    def dist_map(a, index):
        i,j = np.indices(a.shape, sparse=True)
        return np.sqrt((i-index[0])**2 + (j-index[1])**2)

    for source in light_sources:
        source.update()
        point_array = [source.x, source.y]
        if source.distance >= 100:
            continue

        # leeres array erstellen (ds = distance-shadow ...
        # because its the distance and shadow and whatever)
        ds = np.zeros(light_map[:, :, 0].shape)
        # distanzen berechnen (danke stack overflow)
        ds = dist_map(ds, point_array)
        # (relevanten) werte auf 0.0 - 1.0 skalieren
        # (manche sind über 1.0, werden nächste zeile gefiltert)
        ds[:, :] = ds[:, :] / source.radius
        # licht beschränken
        ds = np.clip(ds, a_min=0, a_max=1)
        # invertieren (kleinere distanz = hellere farbe)
        ds = 1 - ds

        for color_channel in COLOR_CHANNELS:
            light_map[:, :, color_channel] = np.maximum(light_map[:, :, color_channel], np.astype(source.color[color_channel] * ds, np.uint8))


def apply_light_map(p):
    
    p[:, :, :] = np.astype(p[:, :, :] * (light_map[:, :, :] / 255), np.uint8)


def crt(f=0.96):

    p = surfarray.pixels3d(s)

    for index, channel in enumerate(COLOR_CHANNELS):
        p[:, index    ::3, channel] = np.astype(p[:, index    ::3, channel] * f, np.uint8)
        p[:, index + 1::3, channel] = np.astype(p[:, index + 1::3, channel] * f, np.uint8)
