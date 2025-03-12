import pygame
import math

class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.pos = pygame.math.Vector2(pos)
        self.speed = 0
        self.health = 0
        
    def move_towards(self, target):
        direction = pygame.math.Vector2(target) - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.pos += direction * self.speed
            self.rect.center = self.pos
    
    def update(self):
        # Ejecutar árbol de comportamiento
        if hasattr(self, 'bt'):
            self.bt.run() 