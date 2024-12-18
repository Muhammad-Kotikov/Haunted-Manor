import os
import pygame
from settings import Resolution

def get_game_folder():
    """
    Returns the path to the root game folder.
    This uses `os.path.dirname` twice to navigate up one directory from the current file.
    """
    return os.path.dirname(os.path.dirname(__file__))

def get_sprite(filename: str):
    """
    Loads a sprite image from the `rsc/sprites` directory.

    Args:
        filename (str): The name of the sprite file to load.

    Returns:
        pygame.Surface: The loaded sprite with alpha channel support for transparency.
    """
    try:
        # `.convert_alpha()` improves performance by converting the image format
        sprite = pygame.image.load(os.path.join(get_game_folder(), f'rsc/sprites/{filename}')).convert_alpha()
        return sprite
    except Exception as e:
        print("ERROR Loading sprite", filename)
        print(e)

def get_map(filename: str):
    """
    Opens a map file from the `rsc/maps` directory in read-text mode.

    Args:
        filename (str): The name of the map file to load.

    Returns:
        file object: The opened file object for the map.
    """
    try:
        return open(os.path.join(get_game_folder(), f'rsc/maps/{filename}'), "rt")
    except Exception as e:
        print("ERROR: Loading map", filename)
        print(e)

def get_full_path(relative_path: str):
    """
    Returns the full path to a resource based on a relative path.

    Args:
        relative_path (str): The relative path to the resource (e.g., `sprites/image.png`).

    Returns:
        str: The full path to the resource within the `rsc` directory.
    """
    return os.path.join(get_game_folder(), f'rsc/{relative_path}')

def play_music(relative_path: str, volume: float, duration: int):
    """
    Plays background music from a given file.

    Args:
        relative_path (str): The relative path to the music file.
        volume (float): The volume level of the music (0.0 to 1.0).
        duration (int): Duration for the music to play (in milliseconds).
    """
    try:
        pygame.mixer.music.load(relative_path)  # Load the music file
        pygame.mixer.music.set_volume(volume)  # Set the volume level
        pygame.mixer.music.play(duration)  # Play the music for the specified duration
    except Exception as e:
        print("ERROR: Playing music", relative_path)
        print(e)

def play_soundeffect(relative_path: str, volume: float):
    """
    Plays a sound effect from a given file.

    Args:
        relative_path (str): The relative path to the sound effect file.
        volume (float): The volume level of the sound effect (0.0 to 1.0).
    """
    try:
        sound_effect = pygame.mixer.Sound(relative_path)  # Load the sound effect
        sound_effect.set_volume(volume)  # Set the volume level
        sound_effect.play()  # Play the sound effect
    except Exception as e:
        print("ERROR: Playing sound effect", relative_path)
        print(e)

def get_mouse_pos():
    """
    Gets the current mouse position adjusted for resolution scaling and offsets.

    Returns:
        tuple: The (x, y) coordinates of the mouse position, scaled and adjusted.
    """
    mouse_x, mouse_y = pygame.mouse.get_pos()  # Get raw mouse position
    # Adjust for resolution scaling and offsets
    mouse_x = int(mouse_x / Resolution.SCALE - Resolution.X_OFFSET)
    mouse_y = int(mouse_y / Resolution.SCALE - Resolution.Y_OFFSET)
    return mouse_x, mouse_y
