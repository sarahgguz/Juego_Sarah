import pygame
from .enemy import Enemy
from ai.behavior_tree import *

class Tank(Enemy):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        self.image = pygame.Surface((35, 35))
        self.image.fill((128, 128, 0))  # Color amarillo oscuro temporal para el Tank
        self.rect = self.image.get_rect(center=pos)
        self.speed = 0.75
        self.health = 4
        self.shoot_timer = 0
        self.shoot_delay = 2000  # 2 segundos entre disparos
        self.setup_behavior_tree()
    
    def setup_behavior_tree(self):
        self.bt = Sequence([
            CheckPlayerDistance(self),
            Selector([
                Sequence([
                    IsPlayerInRange(self),
                    ShootAtPlayer(self)
                ]),
                Sequence([
                    IsPlayerClose(self),
                    MaintainDistance(self)
                ]),
                Patrol(self)
            ])
        ])
    
    def shoot(self):
        if pygame.time.get_ticks() - self.shoot_timer > self.shoot_delay:
            self.shoot_timer = pygame.time.get_ticks()
            direction = pygame.math.Vector2(
                self.game.level.player.rect.centerx - self.rect.centerx,
                self.game.level.player.rect.centery - self.rect.centery
            ).normalize()
            Projectile(self.game.level.projectiles, self.rect.center, direction) 