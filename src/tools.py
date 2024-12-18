import os
import pygame
from settings import Resolution

def get_game_folder():
    """
    Returns the Gamefolder
    """
    # os.path.dirname() is weird
    return os.path.dirname(os.path.dirname(__file__))


def get_sprite(filename: str):

    try:
        # das ".convert" sorgTilet für bessere Performanz laut Tutorial und Pygame docs
        # muss man nicht verstehen xD, ".convert_alpha für Bilder mit Alpha Kanal (Tranzparenz für normal Sterbliche)
        sprite = pygame.image.load(os.path.join(get_game_folder(), f'rsc/sprites/{filename}')).convert_alpha()
        return sprite
            
    except Exception as e:
        print("ERROR Loading sprite", filename)
        print(e)


def get_map(filename: str):

    try:
        return open(os.path.join(get_game_folder(), f'rsc/maps/{filename}'), "rt")
    
    except:
        print("ERROR: Loading map ", filename)


def get_full_path(relative_path: str):

    return os.path.join(get_game_folder(), f'rsc/{relative_path}')

def play_music(relative_path: str, volume: float, duration: int):
    pygame.mixer.music.load(relative_path)  
    pygame.mixer.music.set_volume(volume)  
    
    return pygame.mixer.music.play(duration)

def play_soundeffect(relative_path: str, volume: float):
    sound_effect = pygame.mixer.Sound(relative_path)
    sound_effect.set_volume(volume)

    return sound_effect.play()

def get_mp(self):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_x = int(mouse_x / Resolution.SCALE - Resolution.X_OFFSET)
    mouse_y = int(mouse_y / Resolution.SCALE - Resolution.Y_OFFSET)
    return mouse_x, mouse_y
