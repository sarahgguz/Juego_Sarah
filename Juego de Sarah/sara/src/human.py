import pygame
import random
import math
from utils.create_sprites import create_human_sprite

class Human(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.image = create_human_sprite()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 1
        self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.pos = pygame.math.Vector2(pos)
        self.animation_timer = 0
        
    def update(self):
        # Movimiento aleatorio
        if random.random() < 0.02:  # 2% de probabilidad de cambiar dirección
            self.direction = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        
        self.pos += self.direction * self.speed
        self.rect.center = self.pos
        
        # Mantener dentro de la pantalla
        screen_rect = pygame.display.get_surface().get_rect()
        if not screen_rect.contains(self.rect):
            # Rebotar en los bordes
            if self.rect.left < 0 or self.rect.right > screen_rect.width:
                self.direction.x *= -1
            if self.rect.top < 0 or self.rect.bottom > screen_rect.height:
                self.direction.y *= -1
            
            # Asegurar que esté dentro de la pantalla
            self.rect.clamp_ip(screen_rect)
            self.pos = pygame.math.Vector2(self.rect.center)
        
        # Animación simple
        self.animation_timer += 1
        if self.animation_timer % 30 == 0:
            # Crear una copia ligeramente diferente para simular animación
            self.image = create_human_sprite() 