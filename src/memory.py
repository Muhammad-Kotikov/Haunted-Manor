import random
import pygame

from settings import Resolution, FRAMERATE

class Memory():

    WHITE       = (255, 255, 255)
    BLACK       = (0, 0, 0)
    GRAY        = (128, 128, 128)
    RED         = (255, 0, 0)

    ROWS        = 2
    COLS        = 2


    def __init__(self):

        self.PIECE_WIDTH     = Resolution.WIDTH // self.COLS
        self.PIECE_HEIGHT    = (Resolution.HEIGHT - 75) // self.ROWS

        self.FONT        = pygame.font.Font(None, 100)
        self.SMALL_FONT  = pygame.font.Font(None, 75)

        self.won                 = False
        self.won_timer           = FRAMERATE * 1
        self.congrats_timer      = FRAMERATE * 3

        self.lost                = False
        self.lost_timer          = FRAMERATE * 3

        self.exit                = False

        self.correct_matrix  = [[0] * self.COLS for _ in range(self.ROWS)]

        self.first_guess     = False
        self.second_guess    = False

        self.first_guess_number  = 0
        self.second_guess_number = 0

        self.matches         = 0
        self.reveal_timer    = 0  
        self.start_time      = pygame.time.get_ticks()
        self.spaces_list     = []
        
    def update(self):

        if self.won and self.won_timer > 0:
            self.won_timer -= 1
            return
        elif self.won_timer <= 0 and self.congrats_timer > 0:
            self.congrats_timer -= 1
            return
        elif self.congrats_timer <= 0:
            self.exit = True
            return
        elif self.lost and self.lost_timer > 0:
            self.lost_timer -= 1
            return
        elif self.lost_timer <= 0:
            self.exit = True
            return

        if self.first_guess and self.second_guess:
            self.reveal_timer += 1

    # Karten ausblenden nach 5 sek
        if self.reveal_timer > FRAMERATE * 0.75:
            if self.check_guesses(self.first_guess_number, self.second_guess_number):
                self.matches += 1
            self.first_guess = False
            self.second_guess = False
            self.first_guess_number = 0
            self.second_guess_number = 0
            self.reveal_timer = 0  

    # Auf Game_over überprüfen
        if self.matches == self.ROWS * self.COLS // 2:
            self.won = True

        # Pygame quitten
        for event in pygame.event.get():

            # Auswahl des Kärtchens 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = self.get_mp()

                col = (mouse_x - 5) // self.PIECE_WIDTH  
                row = (mouse_y - 80) // self.PIECE_HEIGHT  

                if 0 <= col < self.COLS and 0 <= row < self.ROWS:
                    idx = col + row * self.COLS

                    if not self.first_guess:
                        self.first_guess, self.first_guess_number = True, idx

                    elif not self.second_guess and idx != self.first_guess_number and self.correct_matrix[row][col] == 0:
                        self.second_guess, self.second_guess_number = True, idx

        
    def render(self):

        self.screen.fill(self.BLACK)

        if self.won and self.won_timer <= 0:
            self.draw_winning_message()
            return
        elif self.lost and self.lost_timer >= 0:
            self.draw_losing_message()
            return
        elif self.exit:
            return
        else:
            self.draw_background()
            self.draw_board()
            self.draw_timer()

        
    def enter(self):
        self.lost            = False
        self.reveal_timer    = 0  
        self.game_timer      = 30 * 1000
        self.spaces_list     = []
        self.generate_board()


    def reset(self):
        self.won                 = False
        self.won_timer           = FRAMERATE * 1
        self.congrats_timer      = FRAMERATE * 3

        self.lost                = False
        self.lost_timer          = FRAMERATE * 3

        self.exit                = False

        self.correct_matrix  = [[0] * self.COLS for _ in range(self.ROWS)]

        self.first_guess     = False
        self.second_guess    = False

        self.first_guess_number  = 0
        self.second_guess_number = 0

        self.matches         = 0
        self.reveal_timer    = 0  
        self.start_time      = pygame.time.get_ticks()
        self.spaces_list     = []

    ### Funktionen
    ####Hintergrund darstellen
    def draw_background(self):
        pygame.draw.rect(self.screen, self.BLACK, [0, 0, Resolution.WIDTH, 75])
        pygame.draw.rect(self.screen, self.GRAY, [0, 75, Resolution.WIDTH, Resolution.HEIGHT])

    ####Zahlen für das Bord generieren
    def generate_board(self):

        options_list    = []
        used_pieces     = []

        for item in range(self.ROWS * self.COLS // 2):
            options_list.append(item)

        for item in range(self.ROWS * self.COLS):
            piece = options_list[random.randint(0, (len(options_list)-1))]
            self.spaces_list.append(piece)

            if piece in used_pieces:
                used_pieces.remove(piece)
                options_list.remove(piece)
            else:
                used_pieces.append(piece)


    ####Spiel darstellen (Karten aufdecken, entferenen, ...)
    def draw_board(self):
        for i in range(self.COLS):
            for j in range(self.ROWS):
                x = i * self.PIECE_WIDTH
                y = j * self.PIECE_HEIGHT

                # Zeichne die weißen Karten
                if self.correct_matrix[j][i] == 0: 
                    piece = pygame.draw.rect(self.screen, self.WHITE, [x + 5, y + 80, self.PIECE_WIDTH -10, self.PIECE_HEIGHT - 10],0, 4)

                # Text auf den Karten darstellen
                elif self.correct_matrix[j][i] == 1: 
                    piece_text = self.FONT.render(str(self.spaces_list[i + j * self.COLS]), True, self.GRAY)
                    self.screen.blit(piece_text, (x + 5 + (self.PIECE_WIDTH - 10) // 2 - piece_text.get_width() // 2, y + 80 + (self.PIECE_HEIGHT - 10) // 2 - piece_text.get_height() // 2))
                
                # Karten entfernen
                elif self.correct_matrix[j][i] == 2:  
                    continue 

                # Karten aufdecken, wenn sie ausgewählt wurden
                if (self.first_guess and self.first_guess_number == i + j * self.COLS) or (self.second_guess and self.second_guess_number == i + j * self.COLS):
                    piece_text = self.FONT.render(str(self.spaces_list[i + j * self.COLS]), True, self.GRAY)
                    self.screen.blit(piece_text, (x + 5 + (self.PIECE_WIDTH - 10) // 2 - piece_text.get_width() // 2, y + 80 + (self.PIECE_HEIGHT - 10) // 2 - piece_text.get_height() // 2))

    ####Spielzüge überprüfen
    def check_guesses(self, first, second):
        if self.spaces_list[first] == self.spaces_list[second]:
            col1, row1 = first % self.COLS, first // self.COLS
            col2, row2 = second % self.COLS, second // self.COLS
            self.correct_matrix[row1][col1] = self.correct_matrix[row2][col2] = 2  
            return True
        else:
            return False

    ####Timer darstellen
    def draw_timer(self):
        passed_time = pygame.time.get_ticks() - self.start_time
        remaining_time = self.game_timer - passed_time
        
        if remaining_time < 0:
            remaining_time = 0
            self.lost = True

        minutes = remaining_time // 60000
        seconds = (remaining_time % 60000) // 1000

        timer_text = f"{minutes:02}:{seconds:02}"
        timer_surface = self.SMALL_FONT.render(timer_text, True, self.WHITE)
        self.screen.blit(timer_surface, (Resolution.WIDTH // 2 - timer_surface.get_width() // 2, 20))

    def draw_winning_message(self):
        winning_text    = self.SMALL_FONT.render("Congratulations!", True, self.WHITE)
        text_rect       = winning_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(winning_text, text_rect)

    def draw_losing_message(self):
        loosing_text    = self.SMALL_FONT.render("GAME OVER!", True, self.RED)
        text_rect       = loosing_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(loosing_text, text_rect)


    def get_mp(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int(mouse_x / Resolution.SCALE - Resolution.X_OFFSET)
        mouse_y = int(mouse_y / Resolution.SCALE - Resolution.Y_OFFSET)

        return mouse_x, mouse_y
