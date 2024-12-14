import pygame 
from settings import Resolution, FRAMERATE


class Kryptex():

    WHITE       = (255, 255, 255)
    BLACK       = (0, 0, 0)
    GRAY        = (150, 150, 150)  
    TARGET_WORD = "AAB"
    SPACING     = 20

    def __init__(self):

        self.FONT        = pygame.font.Font(None, 200)
        self.SMALL_FONT  = pygame.font.Font(None, 100)

        self.won                 = False
        self.won_timer           = FRAMERATE * 1
        self.congrats_timer      = FRAMERATE * 3
        self.exit                = False

        self.mouse_pos           = (0, 0)
        self.letters             = []

        letter_width        = self.FONT.size("A")[0]

        ### Position Buchstaben
        x                   = Resolution.WIDTH // 2 - (len(self.TARGET_WORD) // 2 * letter_width + len(self.TARGET_WORD) // 2 * self.SPACING)
        y                   = Resolution.HEIGHT // 2

        for letter in ["A"] * len(self.TARGET_WORD):
            self.letters.append({
                "char"  : letter,
                "index" : 0,
                "pos"   : (x, y)
            })
            x += letter_width + self.SPACING

        self.selected_letter = None
    

    def update(self):

        if self.won and self.won_timer > 0:
            self.won_timer -= 1
            self.selected_letter = None
            return
        elif self.won_timer <= 0 and self.congrats_timer > 0:
            self.congrats_timer -= 1
            return
        elif self.congrats_timer <= 0:
            self.exit = True
            return
    
        self.mouse_pos = self.get_mp()

        for event in pygame.event.get():         

            if event.type == pygame.MOUSEBUTTONDOWN:
                for p, letter in enumerate(self.letters):
                    letter_surface = self.FONT.render(letter["char"], True, self.GRAY if self.selected_letter == p else self.WHITE)
                    letter_rect = letter_surface.get_rect(center=letter["pos"])

                    if letter_rect.collidepoint(self.mouse_pos):  
                        self.selected_letter = p if self.selected_letter != p else None
                        break

            elif event.type == pygame.MOUSEWHEEL and self.selected_letter is not None:                                                     #         
                self.letters[self.selected_letter]["index"] = (self.letters[self.selected_letter]["index"] + event.y) % 26                                                  #
                self.letters[self.selected_letter]["char"] = chr(self.letters[self.selected_letter]["index"] + ord('A'))                                                    #
                                                                                                                                                        #
                # Überprüfung der Zeichenkette ermöglichen                                                                                                        #
                current_text = ''.join([letter["char"] for letter in self.letters]) 
    
                if current_text == self.TARGET_WORD:                                                                                
                    self.won = True


    def render(self):
        self.screen.fill(self.BLACK)

        if self.won and self.won_timer <= 0:
            self.draw_winning_message()
            return
        elif self.exit:
            return
        else:
            self.draw_letters()


    def draw_winning_message(self):
        winning_text    = self.SMALL_FONT.render("Congratulations!", True, self.WHITE)
        text_rect       = winning_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(winning_text, text_rect)

    ####Buchstaben anzeigen
    def draw_letters(self):
        for p, letter in enumerate(self.letters):
            color           = self.GRAY if self.selected_letter == p else self.WHITE
            letter_surface  = self.FONT.render(letter["char"], True, color)
            letter_rect     = letter_surface.get_rect(center=letter["pos"])
            self.screen.blit(letter_surface, letter_rect)


    def get_mp(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int(mouse_x / Resolution.SCALE - Resolution.X_OFFSET)
        mouse_y = int(mouse_y / Resolution.SCALE - Resolution.Y_OFFSET)

        return mouse_x, mouse_y