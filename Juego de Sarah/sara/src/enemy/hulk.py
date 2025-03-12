import pygame
import random
from ai.behavior_tree import Sequence, Selector, CheckPlayerDistance, ChasePlayer, Patrol
from utils.create_sprites import create_hulk_sprite

class Hulk(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.image = create_hulk_sprite()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 1.0
        self.health = 3
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(1, 0)
        self.distance_to_player = float('inf')
        self.setup_behavior_tree()
    
    def setup_behavior_tree(self):
        self.bt = Sequence([
            CheckPlayerDistance(self),
            Selector([
                ChasePlayer(self),
                Patrol(self)
            ])
        ])
    
    def update(self):
        self.bt.run()
        
        # Efecto visual según la salud
        if self.health <= 2:
            # Tinte más rojizo cuando está dañado
            tinted = self.original_image.copy()
            tinted.fill((255, 100, 100), special_flags=pygame.BLEND_RGB_MULT)
            self.image = tinted
    
    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False 