# Import necessary modules from pygame and other packages
from pygame import key, Vector2  # `key` for handling keypresses, `Vector2` for direction vectors
from copy import deepcopy  # To make deep copies of objects
from settings import key_map  # Import custom key mappings from settings

from entities.creature import CommandDirection  # Import CommandDirection class from creature module

# Define the InputHander class, which processes player input
class InputHander():

    # Constructor that initializes necessary attributes for input handling
    def __init__(self, player):
        # Initialize the CommandDirection object with the player
        self.cmd = CommandDirection(player)

        # Initialize vector for the direction that the player is pressing
        self.pressed_direction = Vector2(0, 0)

        # Initialize counters for tracking when keys were last pressed
        self.last_left = 0
        self.last_right = 0
        self.last_up = 0
        self.last_down = 0

        # Store the current key states (whether keys are pressed or not)
        self.keys_pressed = key.get_pressed()

    # Method to check if a particular key is pressed
    def pressed(self, key: key):
        return self.keys_pressed[key]

    # Method to check if a particular key was just pressed (not held)
    def just_pressed(self, key: key):
        return self.keys_pressed[key] and not self.keys_last[key]

    # Method to check if a particular key was just released (from being pressed)
    def just_released(self, key: key):
        return not self.keys_pressed[key] and self.keys_last[key]

    # Method to update the key states by comparing current and last frame key states
    def update_keys(self):
        """
        Gets the current key states, compares them to the states of the last frame and updates corresponding lists accordingly
        """
        # Save the previous key states (deep copy to avoid reference issues)
        self.keys_last = deepcopy(self.keys_pressed)

        # Update the current key states
        self.keys_pressed = key.get_pressed()

        # Update the target direction based on the new input states
        self.get_target_direction()

    # Method to determine the direction the player wants to move
    def get_target_direction(self):
        """
        Determines the direction the player wants to move to, by interpreting current and past inputs
        """

        # Function to determine movement direction for one axis (either x or y)
        def get_target_direction_for_axis(neg, pos, last_neg, last_pos):
            """
            Given two buttons and the frame length since they were last pressed, determines the direction the player intends to move
            """

            # Case when neither button is pressed
            if not self.pressed(neg) and not self.pressed(pos):
                return 0

            # Case when only the negative direction is pressed
            if self.pressed(neg) and not self.pressed(pos):
                return -1

            # Case when only the positive direction is pressed
            if not self.pressed(neg) and self.pressed(pos):
                return 1

            # Case when both buttons are pressed but negative was pressed first
            elif last_neg < last_pos:
                return -1

            # Case when both buttons are pressed at the same time or positive was pressed first
            else:
                return 1

        # Helper function to count the frames since a button was last pressed
        def count_last(button, counter):
            # If the button was just pressed, reset the counter to 0
            if self.just_pressed(button):
                return 0
            else:
                # Otherwise, increment the counter by 1
                return counter + 1

        # Initialize a vector to hold the final pressed direction (x, y)
        pressed_direction = Vector2(0, 0)

        # Update the "last pressed" counters for each directional button
        self.last_left = count_last(key_map["left"], self.last_left)
        self.last_right = count_last(key_map["right"], self.last_right)
        self.last_up = count_last(key_map["up"], self.last_up)
        self.last_down = count_last(key_map["down"], self.last_down)

        # Determine the movement direction on the x-axis based on the input
        pressed_direction.x = get_target_direction_for_axis(key_map["left"], key_map["right"], self.last_left, self.last_right)

        # Determine the movement direction on the y-axis based on the input
        pressed_direction.y = get_target_direction_for_axis(key_map["up"], key_map["down"], self.last_left, self.last_right)

        # Execute the command to move the player in the determined direction
        self.cmd.execute(pressed_direction)
