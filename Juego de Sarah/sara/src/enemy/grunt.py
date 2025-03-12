import pygame
import random
from ai.behavior_tree import Sequence, Selector, CheckPlayerDistance, ChasePlayer, Patrol
from utils.create_sprites import create_grunt_sprite

class Grunt(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.image = create_grunt_sprite()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 1.5  # Velocidad reducida
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

        # Movimiento simple hacia el jugador
        player_pos = pygame.math.Vector2(self.game.level.player.rect.center)
        direction = player_pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.pos += direction * self.speed
            self.rect.center = self.pos 