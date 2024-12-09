from pygame import key, Vector2
from copy import deepcopy
from settings import key_map


class InputHander():

    def __init__(self):
        self.pressed_direction = Vector2(0, 0)
        self.last_left = 0
        self.last_right = 0
        self.last_up = 0
        self.last_down = 0

        self.keys_pressed = key.get_pressed()

    def pressed(self, key: key):
        return self.keys_pressed[key]
    
    def just_pressed(self, key: key):
        return self.keys_pressed[key] and not self.keys_last[key]
    
    def just_released(self, key: key):
        return not self.keys_pressed[key] and self.keys_last[key]

    def update_keys(self):
        """
        Gets the current key states, compares them to the states of the last frame and updates corresponding lists accordingly
        """

        self.keys_last = deepcopy(self.keys_pressed)
        self.keys_pressed = key.get_pressed()


    def get_target_direction(self):
        """
        Determines the direction the player wants to move to, by interpreting current and past inputs
        """

        def get_target_direction_for_axis(neg, pos, last_neg, last_pos):
            """
            Given two buttons and the frame length since they were last pressed, determines the direction the player intents to move
            """

            # nothing pressed
            if not self.pressed(neg) and not self.pressed(pos):
                return 0
            
            # only negative pressed
            if self.pressed(neg) and not self.pressed(pos):
                return -1
            
            # only positive pressed
            if not self.pressed(neg) and self.pressed(pos):
                return 1
            
            # both pressed but negative was pressed later
            elif last_neg < last_pos:
                return -1
            
            # both pressed at same time or positive later
            else:
                return 1
            
        def count_last(button, counter):
            # if the button was just pressed, the last press is 0 frames ago
            if self.just_pressed(button):
                return 0
            else:
                # else just count up
                return counter + 1
            
        pressed_direction = Vector2(0, 0)
            
        self.last_left = count_last(key_map["left"], self.last_left)
        self.last_right = count_last(key_map["right"], self.last_right)
        self.last_up = count_last(key_map["up"], self.last_up)
        self.last_down = count_last(key_map["down"], self.last_down)
        
        pressed_direction.x = get_target_direction_for_axis(key_map["left"], key_map["right"], self.last_left, self.last_right)
        pressed_direction.y = get_target_direction_for_axis(key_map["up"], key_map["down"], self.last_left, self.last_right)

        if pressed_direction.length() != 0:
            pressed_direction.normalize()
        
        return pressed_direction