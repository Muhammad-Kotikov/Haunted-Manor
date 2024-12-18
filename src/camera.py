import pygame
from entity import Entity

# Constants to control camera behavior
MAX_DISTANCE_TO_TARGET = 18  # Maximum allowed distance between camera and target before recentering
TIME_UNTIL_RECENTER = 45     # Time in frames to wait before automatically recentering the camera

# Create a shorthand for 2D vector operations using Pygame's Vector2
vec = pygame.Vector2

class Camera:
    """
    A class to manage a camera view that follows a target entity, with boundaries and smoothing.
    """
    def __init__(self, rect: pygame.Rect, boundaries: pygame.Rect | None, target: Entity | None):
        """
        Initialize the Camera.

        Args:
            rect (pygame.Rect): The camera's viewport rectangle.
            boundaries (pygame.Rect | None): Optional boundaries to restrict camera movement.
            target (Entity | None): The entity that the camera will follow.
        """
        self.position = vec(0, 0)  # Camera's current position in the world
        if target:
            # Center the camera on the target if it exists
            self.position = vec(target.rect.centerx - rect.width / 2, target.rect.centery - rect.height / 2)
        self.last_pos = self.position  # Store the last position for smoothing
        self.rect = rect  # The camera's viewport rectangle
        self.target = target  # The entity the camera follows
        self.boundaries = boundaries  # Optional boundaries for camera movement
        self.timer = 0  # Timer to track how long the target has been stationary

    def update(self):
        """
        Update the camera's position based on the target's movement and apply smoothing.
        """
        # Smoothstep function for smoothing transitions
        def smoothstep(t: float):
            v1 = t ** 2
            v2 = 1.0 - (1.0 - t) ** 2
            return pygame.math.lerp(v1, v2, t)

        # Calculate the target's position relative to the camera's viewport
        new_pos = vec(0, 0)
        new_pos.x = self.target.rect.centerx - self.rect.width / 2
        new_pos.y = self.target.rect.centery - self.rect.height / 2

        if self.target:
            # Clamp the camera's position within a maximum distance from the target
            self.position.x = pygame.math.clamp(self.position.x, new_pos.x - MAX_DISTANCE_TO_TARGET, new_pos.x + MAX_DISTANCE_TO_TARGET)
            self.position.y = pygame.math.clamp(self.position.y, new_pos.y - MAX_DISTANCE_TO_TARGET, new_pos.y + MAX_DISTANCE_TO_TARGET)

        # If the target is stationary, increment the timer
        if self.target.velocity.length() == 0:
            self.timer += 1
        else:
            # Reset the timer when the target moves
            self.timer = 0

        # Smoothly recenter the camera if the timer exceeds the threshold
        if self.timer >= TIME_UNTIL_RECENTER:
            self.position.x = pygame.math.lerp(self.last_pos.x, new_pos.x, 0.08)
            self.position.y = pygame.math.lerp(self.last_pos.y, new_pos.y, 0.08)
        else:
            # Update the last position if not recentering
            self.last_pos = self.position

        # Restrict the camera's position within the boundaries (if provided)
        if self.boundaries:
            self.position.x = pygame.math.clamp(self.position.x, self.boundaries.x, self.boundaries.width - self.rect.width)
            self.position.y = pygame.math.clamp(self.position.y, self.boundaries.y, self.boundaries.height - self.rect.height)

        # Update the camera's rectangle to reflect the new position
        self.rect.x = round(self.position.x)
        self.rect.y = round(self.position.y)

    def render(self, screen):
        pass
