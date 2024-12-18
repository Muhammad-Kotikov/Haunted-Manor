import pygame
from settings import Resolution, key_map
from tools import get_full_path

class Dialogue:

    FRAMES_PER_LETTER = 6  # Number of frames to wait before revealing the next letter in the dialogue

    def __init__(self, text=[], sprites=[]):
        """
        Initializes the Dialogue object.
        
        Args:
            text (list): A list of strings representing the dialogue text for each phase.
            sprites (list): A list of sprite images corresponding to each phase of the dialogue.
        """
        self.SMALL_FONT = pygame.font.Font(get_full_path("fonts/minecraft_font.ttf"), 7)  # Loads a small pixelated font
        self.phase = 0  # Current phase of the dialogue
        self.text = text  # Full dialogue text for all phases
        self.shown_text = ""  # The text currently shown on screen
        self.text_amount = 0  # Number of letters currently revealed
        self.text_frame = 0  # Frame counter for letter reveal timing
        self.sprites = sprites  # List of sprites to display during each phase
        self.done = False  # Indicates if the dialogue is complete

    def update(self):
        """
        Updates the state of the dialogue, including text progression and handling user input.
        """
        if self.phase == len(self.text):  # Check if all phases of dialogue are complete
            self.done = True
            return
        
        # Increment text_frame and reveal the next letter if needed
        if self.text_amount < len(self.text[self.phase]):
            self.text_frame = (self.text_frame + 1) % self.FRAMES_PER_LETTER

        # Reveal the next letter when the frame count reaches 0
        if self.text_frame == 0 and self.text_amount < len(self.text[self.phase]):
            self.text_amount += 1
        
        # Handle events for quitting or advancing dialogue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle quit event
                self.exit = True
            if event.type == pygame.KEYDOWN and event.key == key_map["dialogue_next"]:  # Advance dialogue on key press
                if self.text_amount < len(self.text[self.phase]):  # Fast-forward to the end of the current phase
                    self.text_amount = len(self.text[self.phase])
                else:  # Move to the next phase
                    self.phase += 1
                    self.text_frame = 0
                    self.text_amount = 0

    def render(self):
        """
        Renders the dialogue text and sprite onto the screen.
        """
        self.screen.fill((0, 0, 0))  # Clear the screen with a black background

        if self.phase < len(self.sprites):  # Check if there are sprites to display for the current phase
            self.text_shown = self.text[self.phase][:self.text_amount]  # Get the portion of text currently revealed
            # Center and render the sprite for the current phase
            self.screen.blit(self.sprites[self.phase], (Resolution.WIDTH // 2 - self.sprites[self.phase].get_width() // 2, 50))

            # Render each line of text, centering it on the screen
            for i, line in enumerate(self.text_shown.split('\n')):
                label = self.SMALL_FONT.render(line, False, (255, 255, 255))  # Render the text line
                self.screen.blit(label, (Resolution.WIDTH // 2 - label.get_width() // 2, 250 + i * (label.get_height() + 2)))  # Center and display the text
