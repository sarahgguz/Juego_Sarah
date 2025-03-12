import pygame
import math
from utils.create_sprites import create_projectile_sprite

class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, pos, direction):
        super().__init__(group)
        self.image = create_projectile_sprite()
        self.rect = self.image.get_rect(center=pos)
        
        self.speed = 10
        self.direction = direction
        self.pos = pygame.math.Vector2(pos)
        
    def update(self):
        # Actualizar posición
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        
        # Eliminar si sale de la pantalla
        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill() 