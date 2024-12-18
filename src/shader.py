# Import necessary modules
from pygame import Surface, surfarray, Vector2  # Importing Pygame Surface for rendering, surfarray for pixel access, and Vector2 for 2D vector calculations
import numpy as np  # Import numpy for numerical operations, particularly for handling arrays
from settings import options  # Import settings options (likely for enabling/disabling features)

# Global variables (initial values)
s = None  # Surface object for rendering
r = None  # Red channel placeholder
g = None  # Green channel placeholder
b = None  # Blue channel placeholder
h = 0  # Height of the screen
w = 0  # Width of the screen

# Constants for color channels
RED_CHANNEL = 0
GREEN_CHANNEL = 1
BLUE_CHANNEL = 2

# List of color channels to be used later
COLOR_CHANNELS = [RED_CHANNEL, GREEN_CHANNEL, BLUE_CHANNEL]

# Light map (array to store light levels across the screen)
light_map = None
# Ambient light color (default or set by user)
ambient_color = None
# List of light sources in the scene
light_sources = []

# Duration for lightning effect (if applicable)
nv_duration = 0

# LightSource class to represent each light source in the scene
class LightSource():

    def __init__(self, position : Vector2, offset : Vector2, radius : int, color : tuple):
        """
        Initialize a new light source with its position, offset, radius, and color.
        Add the light source to the global `light_sources` list.
        """
        self.position = position  # Light source position in the world
        self.radius = radius  # Light source radius
        self.color = color  # Light source color (RGB tuple)
        self.offset = offset  # Offset from the camera (for proper positioning)
        self.distance = 0  # Distance of the light source from the camera
        light_sources.append(self)  # Add the new light source to the global list

    def update(self, radius = None, color = None):
        """
        Update the light source properties (position, radius, color).
        This method also calculates the distance from the camera and adjusts the position.
        """
        # Adjust the light source position based on camera position and offset
        self.x = round(self.position.x - camera.position.x + self.offset.x)
        self.y = round(self.position.y - camera.position.y + self.offset.y)

        # Calculate the distance from the camera to the light source
        self.distance = Vector2(self.position.x - camera.rect.centerx + self.offset.x, 
                                self.position.y - camera.rect.centery + self.offset.y).length()

        # Update the radius if provided
        if radius != None:
            self.radius = radius
        
        # Update the color if provided
        if color != None:
            self.color = color

# Initialize function to set up the screen, camera, and other light-related parameters
def init(screen : Surface, c, a = (25, 10, 10)):
    """
    Initialize global variables related to screen, camera, and light map.
    Also initializes the ambient light color.
    """
    global camera  # Global camera reference
    global s, p  # Surface and pixel array references
    global w, h  # Screen width and height
    global light_map  # Light map array
    global r, g, b  # Color channels
    global ambient_color  # Ambient light color

    camera = c  # Set the camera reference
    ambient_color = a  # Set the ambient light color

    s = screen  # Set the surface (screen) for rendering
    h = screen.get_height()  # Set the height of the screen
    w = screen.get_width()  # Set the width of the screen

    light_map = np.zeros(shape=(w, h, 3)).astype(np.uint8)  # Create a light map with initial zero values

# Lightning function to apply lighting effects if enabled in options
def lightning():
    """
    Applies the lightning effect and updates the light map.
    If lightning is disabled, it does nothing.
    """
    if not options['lightsystem']:  # If the light system is disabled in options, do nothing
        return

    global nv_duration  # Global variable for lightning duration

    if nv_duration > 0:
        ac = (200, 200, 200)  # Set ambient color for lightning effect
    else:
        ac = ambient_color  # Use normal ambient color

    # Get the pixel array from the surface (to modify pixel colors)
    p = surfarray.pixels3d(s)
    reset(ac)  # Reset the light map with the ambient color
    apply_light_sources()  # Apply the light sources to the light map
    apply_light_map(p)  # Apply the final light map to the pixel array
    nv_duration -= 1  # Decrease the lightning duration counter

# Reset the light map to a given ambient color
def reset(ac = ambient_color):
    """
    Resets the light map to the ambient color.
    """
    for channel in COLOR_CHANNELS:
        light_map[:, :, channel] = ac[channel]  # Set all pixels in the light map to the ambient color for each channel

# Distance map function to calculate distances from a point
def dist_map(a, index, radius):
    """
    Creates a map of distances from a given point (index) within a specified radius.
    This is used for determining the intensity of the light source in a region.
    """
    i,j = np.indices(a.shape, sparse=True)  # Create indices for the array
    return np.sqrt((i-index[0])**2 + (j-index[1])**2) / radius  # Return the distance map (normalized)

# Apply light sources to the light map
def apply_light_sources():
    """
    Applies all light sources to the light map based on their properties.
    """
    for source in light_sources:  # Iterate over each light source

        source.update()  # Update the light source properties (position, color, radius)

        if source.distance >= 200:  # If the light source is too far, skip it
            continue

        # Calculate the starting and ending points for the light source's effect
        start_x = max(source.x - source.radius, 0)
        start_y = max(source.y - source.radius, 0)

        end_x = min(source.x + source.radius, w)
        end_y = min(source.y + source.radius, h)

        if start_x > end_x or start_y > end_y:  # If the range is invalid, skip
            continue

        # Create a sub-distance map for the region affected by the light source
        sub_ds = dist_map(np.zeros((end_x - start_x, end_y - start_y)), (source.x - start_x, source.y - start_y), source.radius)

        # Normalize the sub-distance map and clip it between 0 and 1
        sub_ds = 1 - np.clip(sub_ds, a_min=0, a_max=1)
        sub_lm = light_map[start_x:end_x, start_y:end_y]  # Get the sub-region of the light map to modify

        # Apply the light intensity for each color channel (red, green, blue)
        for color_channel in COLOR_CHANNELS:
            sub_lm[:,:,color_channel] = np.maximum(sub_lm[:,:,color_channel], np.astype(source.color[color_channel] * sub_ds, np.uint8))

# Apply the light map to the pixel array (update the surface)
def apply_light_map(p):
    """
    Applies the light map to the screen by modifying the pixel array.
    """
    p[:, :, :] = np.astype(p[:, :, :] * (light_map[:, :, :] / 255), np.uint8)  # Multiply each pixel by the light map's color values

# CRT effect function (applies CRT filter if enabled)
def crt(f=0.96):
    """
    Applies a CRT filter effect to the screen pixels.
    """
    if not options['crt']:  # If the CRT effect is disabled in options, do nothing
        return

    p = surfarray.pixels3d(s)  # Get the pixel array from the surface

    for index, channel in enumerate(COLOR_CHANNELS):  # Iterate over each color channel (RGB)
        # Apply the CRT effect to each color channel, reducing intensity at every 3rd pixel
        p[:, index    ::3, channel] = np.astype(p[:, index    ::3, channel] * f, np.uint8)
        p[:, index + 1::3, channel] = np.astype(p[:, index + 1::3, channel] * f, np.uint8)
