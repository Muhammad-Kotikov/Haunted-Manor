import pygame
from entity.tile.tile import Tile
from entity.creature.player.player import Player

# Traptypes:
CYCLING = 1     # this kind of traps just repeats one action over and over again
DETECTING = 2   # this kind of trap waits for the player to move 

# trap_properties for cycling traps look like this:
# [(x1, y1, w1, h1, d1), (x2, y2, w2, h2, d2)]
# any xi, yi describe the position and any wi and hi describe the size of the hitbox
# which determines whether the player gets hit, di describes how long that hitbox is active

class Trap(Tile):

    def __init__(self, trap_type, trap_properties, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.trap_type = trap_type
        self.trap_properties = trap_properties
        
        if self.trap_type == CYCLING:
            self.phase = 0
            self.frame = 0
            self.update_hitbox()
    

    def update(self):

        if self.world.player != None and self.collision_box.colliderect(self.world.player.rect):
            self.world.player.hit(1)

        if self.trap_type == CYCLING:
            self.frame += 1

        if self.frame >= self.phase_duration:
            self.frame = 0
            self.phase = (self.phase + 1) % len(self.trap_properties)
            self.update_hitbox()
        


    def render(self, screen, camera):
        super().render(screen, camera)
        hit_surface = pygame.Surface((self.collision_box.width, self.collision_box.height))
        hit_surface.fill((255, 255, 0))
        screen.blit(hit_surface, (self.collision_box.x - camera.rect.x, self.collision_box.y - camera.rect.y))


    def update_hitbox(self):

        if self.trap_type == CYCLING:
            x = self.position.x + self.trap_properties[self.phase][0]
            y = self.position.y + self.trap_properties[self.phase][1]
            w = self.trap_properties[self.phase][2]
            h = self.trap_properties[self.phase][3]
            self.phase_duration = self.trap_properties[self.phase][4]
            self.collision_box = pygame.Rect(x, y, w, h)

    
    def copy(self, x, y):

        return Trap(self.trap_type, self.trap_properties, self.has_collision, self.sprite, x, y, self.rect.width, self.rect.height)
    
