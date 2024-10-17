import pygame
from creature import Creature

MAX_SPEED = 100
ACCELERATION = MAX_SPEED / 6
DECELERATION = MAX_SPEED / 4


class Player(Creature):

    def __init__(self, keys, keys_last):
        self.velocity_x = 0, self.velocity_y = 0
        self.acceleration_x = 0, self.acceleration_y = 0

        self.keys = keys
        self.keys_last = keys_last

    def control(self):
        
        pass

    def update(self, dt):
        pass

    def render(self):
        pass