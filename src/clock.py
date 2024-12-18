#   Mithilfe von: https://www.youtube.com/watch?v=bmLuz8ISn20 erstellt
#   Quelle Bild: https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.flume.de%2Fde%2Fgrossuhr-ersatzteile%2Fzifferblaetter-zubehoer%2Fzifferblaetter%2Froemische-zahlen%2Fzifferblatt-aluminium-roemische-zahlen-oe-178-mm%2F334966&psig=AOvVaw09Nzh0TlKbj4LI5cwo9fmX&ust=1731253425590000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCLibot7Lz4kDFQAAAAAdAAAAABAE
#   Das Bild wurde eigenständig an die Bedürfnisse angepasst

#   Vorbereitung
##  Allgemeine Vorbereitung
### Module und Abhängigkeiten importieren 
import pygame
import math

from settings import Resolution, FRAMERATE
from tools import get_sprite

class Clock():

    def __init__(self):

        self.WHITE   = (255, 255, 255)
        self.BLACK   = (0, 0, 0)
        self.RED     = (255, 0, 0)

        self.CENTER          = (Resolution.WIDTH // 2, Resolution.HEIGHT // 2)
        self.C_WIDTH         = Resolution.WIDTH // 2
        self.C_HEIGHT        = Resolution.HEIGHT // 2
        self.RADIUS          = 250

        ### Zeiger-Positionen

        self.TARGET_HOUR         = math.radians(360 * (3 / 12))    
        self.TARGET_MINUTE       = math.radians(360 * (30 / 60))   
        self.TARGET_SECOND       = math.radians(360 * (15 / 60))   

        self.ANGLE_TOLERANCE     = 0.1

        self.angle_hour          = math.radians(360 * (1 / 12)) 
        self.angle_minute        = math.radians(360 * (30 / 60)) 
        self.angle_second        = math.radians(360 * (15 / 60))

        self.FONT                = pygame.font.Font(None, 100)
        self.BACKGROUND_IMAGE    = get_sprite('minigame_clock_image.png')
        self.selected_clockhand  = None

        self.won                 = False
        self.won_timer           = FRAMERATE * 1
        self.congrats_timer      = FRAMERATE * 3
        self.exit                = False

        self.mouse_pos           = (0, 0)

        self.offset_hour = 0
        self.offset_minute = 0
        self.offset_second = 0

    
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

        if self.check_time():
            self.won = True

        if self.won == False:
            self.exit = False

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.exit = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
                mouse_x, mouse_y = self.get_mp()

                if self.chose_clockhand(self.angle_hour, self.RADIUS * 0.5, (mouse_x, mouse_y)):
                    self.selected_clockhand = 'hour'
                    # Startwinkel
                    self.offset_hour = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0]) - self.angle_hour
                
                elif self.chose_clockhand(self.angle_minute, self.RADIUS * 0.75, (mouse_x, mouse_y)):
                    self.selected_clockhand = 'minute'
                    # Startwinkel
                    self.offset_minute = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0]) - self.angle_minute

                elif self.chose_clockhand(self.angle_second, self.RADIUS * 1, (mouse_x, mouse_y)):
                    self.selected_clockhand = 'second'
                    # Startwinkel
                    self.offset_second = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0]) - self.angle_second

            elif event.type == pygame.MOUSEBUTTONUP:
                if self.selected_clockhand:
                    self.selected_clockhand = None 

            elif event.type == pygame.MOUSEMOTION and self.selected_clockhand:
                mouse_x, mouse_y = self.get_mp()
                angle = math.atan2(mouse_y - self.CENTER[1], mouse_x - self.CENTER[0])

                if self.selected_clockhand == 'hour':
                    self.angle_hour = angle - self.offset_hour

                elif self.selected_clockhand == 'minute':
                    self.angle_minute = angle - self.offset_minute

                elif self.selected_clockhand == 'second':
                    self.angle_second = angle - self.offset_second

    def render(self):

        self.screen.fill(self.BLACK)

        if self.won and self.won_timer <= 0:
            self.draw_winning_message()
            return
        elif self.exit:
            return

        # Hintergrundbild
        self.screen.blit(self.BACKGROUND_IMAGE, (0, 0))

        # Stundenzeiger
        x_hour = self.C_WIDTH + self.RADIUS * 0.5 * math.cos(self.angle_hour - math.pi / 2)
        y_hour = self.C_HEIGHT + self.RADIUS * 0.5 * math.sin(self.angle_hour - math.pi / 2)
        pygame.draw.line(self.screen, self.BLACK, self.CENTER, (x_hour, y_hour), 12)

        # Minutenzeiger
        x_minute = self.C_WIDTH + self.RADIUS * 0.75 * math.cos(self.angle_minute - math.pi / 2)
        y_minute = self.C_HEIGHT + self.RADIUS * 0.75 * math.sin(self.angle_minute - math.pi / 2)
        pygame.draw.line(self.screen, self.BLACK, self.CENTER, (x_minute, y_minute), 8)

        # Sekundenzeiger
        x_second = self.C_WIDTH + self.RADIUS * 1 * math.cos(self.angle_second - math.pi / 2)
        y_second = self.C_HEIGHT + self.RADIUS * 1 * math.sin(self.angle_second - math.pi / 2)
        pygame.draw.line(self.screen, self.RED, self.CENTER, (x_second, y_second), 3)

        # Mittelpunkt
        pygame.draw.circle(self.screen, self.BLACK, self.CENTER, 20) 

    
    def enter(self):
        pass


    def exit(self):
        pass


    def chose_clockhand(self, clockhand_angle, radius, mouse_pos):
        """
        clockhand_x = self.C_WIDTH + radius * math.cos(clockhand_angle - math.pi / 2)
        clockhand_y = self.C_HEIGHT + radius * math.sin(clockhand_angle - math.pi / 2)
        """

        num_points = 20  
        for i in range(num_points + 1):
            # Position jedes Punkts entlang des Zeigers
            current_x = self.C_WIDTH + (radius * i / num_points) * math.cos(clockhand_angle - math.pi / 2)
            current_y = self.C_HEIGHT + (radius * i / num_points) * math.sin(clockhand_angle - math.pi / 2)
            
            # Abstand von Punkt zu Maus berechnen
            distance = math.sqrt((mouse_pos[0] - current_x)**2 + (mouse_pos[1] - current_y)**2)
            
            # Wenn der Abstand zu einem Punkt entlang des Zeigers klein genug ist, haben wir einen Treffer
            if distance < 20:  
                return True
        
        return False


    def draw_winning_message(self):
        winning_text    = self.FONT.render("Congratulations!", True, self.WHITE)
        text_rect       = winning_text.get_rect(center=(Resolution.WIDTH // 2, Resolution.HEIGHT // 2))
        self.screen.blit(winning_text, text_rect)


    def check_time(self):

        if (self.TARGET_HOUR - self.ANGLE_TOLERANCE < self.angle_hour   < self.TARGET_HOUR   + self.ANGLE_TOLERANCE) and \
        (self.TARGET_MINUTE  - self.ANGLE_TOLERANCE < self.angle_minute < self.TARGET_MINUTE + self.ANGLE_TOLERANCE) and \
        (self.TARGET_SECOND  - self.ANGLE_TOLERANCE < self.angle_second < self.TARGET_SECOND + self.ANGLE_TOLERANCE):
            return True
        
        return False
    

    def get_mp(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x = int(mouse_x / Resolution.SCALE - Resolution.X_OFFSET)
        mouse_y = int(mouse_y / Resolution.SCALE - Resolution.Y_OFFSET)

        return mouse_x, mouse_y

