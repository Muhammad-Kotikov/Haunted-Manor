import pygame
from settings import TILE_SIZE  # Import the default tile size for consistent scaling across entities

vec = pygame.math.Vector2  # Alias for the 2D vector class in Pygame

class Entity:
    """
    Represents a game entity, including its position, appearance (sprite), and bounding box (rect).
    """

    def __init__(self, sprite: pygame.sprite, x: float = 0, y: float = 0, width: int = TILE_SIZE, height: int = TILE_SIZE):
        """
        Initializes the Entity with its sprite, position, and dimensions.

        Args:
            sprite (pygame.sprite): The sprite representing the visual appearance of the entity.
            x (float): The initial x-coordinate of the entity's position.
            y (float): The initial y-coordinate of the entity's position.
            width (int): The width of the entity's bounding box.
            height (int): The height of the entity's bounding box.
        """
        self.position = vec(x, y)  # The precise position of the entity in the game world
        self.sprite = sprite  # The current sprite image for rendering
        self.original = self.sprite.copy()  # A copy of the original sprite for restoring later
        self.rect = pygame.Rect(x, y, width, height)  # The bounding rectangle of the entity

    def update(self):
        """
        Updates the entity's rectangular position to match its precise vector position.
        """
        self.rect.x = round(self.position.x)  # Update the x-coordinate of the rect
        self.rect.y = round(self.position.y)  # Update the y-coordinate of the rect

    def render(self, screen, camera):
        """
        Draws the entity's sprite on the screen relative to the camera's position.

        Args:
            screen: The Pygame surface where the entity will be drawn.
            camera: The camera object, used to offset the entity's position for rendering.
        """
        # Blit the sprite at the adjusted position (camera-relative coordinates)
        screen.blit(self.sprite, (round(self.rect.x - camera.rect.x), round(self.rect.y - camera.rect.y)))

    def tint(self, color, flag):
        """
        Applies a color tint to the entity's sprite.

        Args:
            color (tuple): The RGB color to apply as the tint.
            flag: A special flag (e.g., `pygame.BLEND_MULT`) for blending the color.

        Reference:
            https://stackoverflow.com/questions/57962130/how-can-i-change-the-brightness-of-an-image-in-pygame
        """
        self.sprite = self.original.copy()  # Restore the sprite to its original state
        self.sprite.fill(color, special_flags=flag)  # Apply the tint with the specified blending flag

    def untint(self):
        """
        Restores the entity's sprite to its original appearance (removing any applied tint).
        """
        self.sprite = self.original  # Reset the sprite to its original state
