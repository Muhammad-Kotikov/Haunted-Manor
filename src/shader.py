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


# https://stackoverflow.com/questions/61628380/calculate-distance-from-all-points-in-numpy-array-to-a-single-point-on-the-basis
def dist_map(a, index, radius):
        i,j = np.indices(a.shape, sparse=True)
        return np.sqrt((i-index[0])**2 + (j-index[1])**2) / radius


def apply_light_sources():

    for source in light_sources:

        source.update()

        if source.distance >= 200:
            continue

        #ds = np.zeros((w, h))

        start_x = max(source.x - source.radius, 0)
        start_y = max(source.y - source.radius, 0)

        end_x = min(source.x + source.radius, w)
        end_y = min(source.y + source.radius, h)

        if start_x > end_x or start_y > end_y:
            continue

        #sub_ds = ds[start_x:end_x, start_y:end_y]
        #sub_ds = np.zeros((end_x - start_x, end_y - start_y))
        sub_ds = dist_map(np.zeros((end_x - start_x, end_y - start_y)), (source.x - start_x, source.y - start_y), source.radius)

        sub_ds = 1 - np.clip(sub_ds, a_min=0, a_max=1)
        sub_lm = light_map[start_x:end_x, start_y:end_y]

        for color_channel in COLOR_CHANNELS:
            sub_lm[:,:,color_channel] = np.maximum(sub_lm[:,:,color_channel], np.astype(source.color[color_channel] * sub_ds, np.uint8))


def apply_light_map(p):
    
    p[:, :, :] = np.astype(p[:, :, :] * (light_map[:, :, :] / 255), np.uint8)


def crt(f=0.96):

    p = surfarray.pixels3d(s)

    for index, channel in enumerate(COLOR_CHANNELS):
        p[:, index    ::3, channel] = np.astype(p[:, index    ::3, channel] * f, np.uint8)
        p[:, index + 1::3, channel] = np.astype(p[:, index + 1::3, channel] * f, np.uint8)
