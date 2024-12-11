import os
import pygame

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
