import pygame

class PlayerState:
    def __init__(self, player):
        self.player = player  # Referenz zum Player-Objekt

    def enter(self):
        """
        Wird aufgerufen, wenn der Zustand aktiviert wird.
        """
        pass

    def exit(self):
        """
        Wird aufgerufen, wenn der Zustand verlassen wird.
        """
        pass

    def update(self, dt):
        """
        Aktualisiert die Logik des Zustands (z. B. Animation).
        """
        pass


class RunningState(PlayerState):
    def enter(self):
        """
        Setzt die Laufanimation basierend auf der Bewegungsrichtung.
        """
        self.player.current_frame = 0  # Animation beginnt beim ersten Frame
        self.player.animation_speed = 0.1  # Geschwindigkeit der Animation
        # Lädt die richtigen Frames basierend auf der Richtung
        self.player.frames = (
            self.player.running_frames_left  # Linkslaufen
            if self.player.target_direction.x < 0
            else [
                pygame.transform.flip(frame, True, False)
                for frame in self.player.running_frames_left
            ]  # Rechtslaufen
        )

    def update(self, dt):
        """
        Aktualisiert die Animation basierend auf der Zeit.
        """
        self.player.current_frame += self.player.animation_speed * dt
        if self.player.current_frame >= len(self.player.frames):
            self.player.current_frame = 0
        # Weist den aktuellen Frame dem Sprite zu
        self.player.sprite = self.player.frames[int(self.player.current_frame)]


class IdleState(PlayerState):
    def enter(self):
        """
        Setzt das Idle-Sprite, wenn der Spieler im Leerlauf ist.
        """
        self.player.sprite = self.player.idle_frame  # Zeigt Standanimation 


class StoppingState(PlayerState):
    def enter(self):
        """
        Setzt das Idle-Sprite, wenn der Spieler anhält.
        """
        self.player.sprite = self.player.idle_frame  # Zeigt Standanimation
