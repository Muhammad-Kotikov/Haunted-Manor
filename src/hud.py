import pygame
from tools import get_full_path

class HUD:
    """
    A class representing the Heads-Up Display (HUD) for the player, including health,
    interactable prompts, and key fragments.
    """

    def __init__(self, target, health_sprite, empty_health_sprite):
        """
        Initializes the HUD with a target entity and health display sprites.

        Args:
            target: The target entity to display HUD information for (e.g., the player).
            health_sprite: The sprite to display for each unit of remaining health.
            empty_health_sprite: The sprite to display for each unit of missing health.
        """
        self.target = target  # The entity the HUD is displaying information for
        self.health_sprite = health_sprite  # Sprite for full health
        self.empty_health_sprite = empty_health_sprite  # Sprite for empty health
        self.SMALL_FONT = pygame.font.Font(get_full_path("fonts/minecraft_font.ttf"), 7)  # Font for HUD text
        self.clock = 0  # A timer for handling periodic updates or animations

    def render(self, screen):
        """
        Renders the HUD elements to the screen, including health, interactables,
        and key fragment information.

        Args:
            screen: The Pygame surface to render the HUD on.
        """
        # If no target is assigned, do nothing
        if self.target is None:
            return

        # Initial offsets and spacing for health bar rendering
        offset_x = 2  # Horizontal offset for the health bar
        offset_y = 2  # Vertical offset for the health bar
        distance_x = 16  # Spacing between health sprites

        # Increment the clock for periodic effects
        self.clock += 1
        if self.clock >= 120:  # Reset the clock after 120 frames
            self.clock = 0

        # Render the health bar with filled health sprites
        for x in range(self.target.health):
            screen.blit(self.health_sprite, (offset_x + distance_x * x, offset_y))

        # Render the health bar with empty health sprites for missing health
        for x in range(self.target.health, self.target.hitpoints):
            screen.blit(self.empty_health_sprite, (offset_x + distance_x * x, offset_y))

        # Display interaction prompt if there are interactables nearby
        if len(self.target.interactables) > 0:
            label = self.SMALL_FONT.render("Press L to interact", False, (255, 255, 255))
            screen.blit(label, (screen.get_width() / 2 - label.get_width() / 2, screen.get_height() * 0.8))

        # Display the number of key fragments if there are any
        if self.target.keys > 0 and not self.target.key_final:
            k_label = self.SMALL_FONT.render(f"Fragments: {self.target.keys}", False, (255, 255, 255))
            screen.blit(k_label, (screen.get_width() - k_label.get_width() - 5, screen.get_height() * 0.03))

        # Display a message indicating the final key has been acquired, flashing every 60 frames
        elif self.target.key_final and self.clock < 60:
            k_label = self.SMALL_FONT.render("Key acquired", False, (255, 255, 255))
            screen.blit(k_label, (screen.get_width() - k_label.get_width() - 5, screen.get_height() * 0.03))
