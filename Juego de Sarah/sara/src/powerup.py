import pygame
import random
from utils.create_sprites import create_powerup_sprite

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, pos, type):
        super().__init__()
        self.game = game
        self.type = type
        self.image = create_powerup_sprite(type)
        self.rect = self.image.get_rect(center=pos)
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 10000  # 10 segundos
        
    def update(self):
        # Hacer que el power-up parpadee cuando está por desaparecer
        current_time = pygame.time.get_ticks()
        time_left = self.lifetime - (current_time - self.creation_time)
        
        if time_left < 3000:  # Últimos 3 segundos
            if (current_time // 200) % 2 == 0:  # Parpadeo cada 200ms
                self.image.set_alpha(100)
            else:
                self.image.set_alpha(255)
        
        # Eliminar si ha pasado el tiempo
        if current_time - self.creation_time > self.lifetime:
            self.kill()
    
    def apply(self, player):
        if self.type == "health":
            player.lives = min(player.lives + 1, 5)
        elif self.type == "speed":
            player.speed_boost_time = pygame.time.get_ticks()
            player.speed_boost_duration = 5000  # 5 segundos
            player.speed = 8
        elif self.type == "shield":
            player.shield_time = pygame.time.get_ticks()
            player.shield_duration = 10000  # 10 segundos
            player.has_shield = True
        elif self.type == "rapid":
            player.rapid_fire_time = pygame.time.get_ticks()
            player.rapid_fire_duration = 5000  # 5 segundos
            player.shoot_delay = 50  # Disparo más rápido 