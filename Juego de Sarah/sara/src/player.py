import pygame
import math
from projectile import Projectile
from utils.create_sprites import create_player_sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.original_image = create_player_sprite()
        self.image = self.original_image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.speed = 5
        self.original_speed = 5
        self.lives = 3
        self.shoot_delay = 150
        self.original_shoot_delay = 150
        self.last_shot = 0
        self.invincible = False
        self.invincible_time = 0
        self.invincible_duration = 2000
        self.rotation = 0
        
        # Power-ups
        self.has_shield = False
        self.shield_time = 0
        self.shield_duration = 0
        self.speed_boost_time = 0
        self.speed_boost_duration = 0
        self.rapid_fire_time = 0
        self.rapid_fire_duration = 0
    
    def update(self):
        current_time = pygame.time.get_ticks()
        
        # Actualizar power-ups
        self.update_powerups(current_time)
        
        # Actualizar invencibilidad
        if self.invincible and current_time - self.invincible_time > self.invincible_duration:
            self.invincible = False
        
        # Hacer parpadear si es invencible
        if self.invincible and (current_time // 100) % 2 == 0:
            self.image.set_alpha(100)
        else:
            self.image.set_alpha(255)
        
        # Movimiento
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.speed
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * self.speed
        
        if dx != 0 or dy != 0:
            # Calcular rotación basada en dirección
            self.rotation = math.degrees(math.atan2(dy, dx))
            # Rotar sprite
            self.image = pygame.transform.rotate(self.original_image, -self.rotation)
            self.rect = self.image.get_rect(center=self.rect.center)
        
        self.pos.x += dx
        self.pos.y += dy
        self.rect.center = self.pos
        self.rect.clamp_ip(self.game.screen.get_rect())
        
        # Disparar
        mouse = pygame.mouse.get_pressed()
        if mouse[0] and current_time - self.last_shot > self.shoot_delay:
            self.shoot()
    
    def update_powerups(self, current_time):
        # Escudo
        if self.has_shield and current_time - self.shield_time > self.shield_duration:
            self.has_shield = False
        
        # Velocidad
        if current_time - self.speed_boost_time > self.speed_boost_duration:
            self.speed = self.original_speed
        
        # Disparo rápido
        if current_time - self.rapid_fire_time > self.rapid_fire_duration:
            self.shoot_delay = self.original_shoot_delay
    
    def shoot(self):
        self.last_shot = pygame.time.get_ticks()
        mx, my = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mx - self.rect.centerx, my - self.rect.centery)
        if direction.length() > 0:
            direction = direction.normalize()
            Projectile(self.game.level.projectiles, self.rect.center, direction)
            self.game.play_sound('shoot')
    
    def take_damage(self):
        if not self.invincible and not self.has_shield:
            self.lives -= 1
            self.invincible = True
            self.invincible_time = pygame.time.get_ticks()
            if self.lives <= 0:
                self.game.game_over()
            return True
        return False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
        # Dibujar escudo si está activo
        if self.has_shield:
            shield_radius = self.rect.width * 0.7
            shield_surf = pygame.Surface((shield_radius*2, shield_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surf, (255, 255, 0, 100), (shield_radius, shield_radius), shield_radius)
            pygame.draw.circle(shield_surf, (255, 255, 255, 150), (shield_radius, shield_radius), shield_radius, 2)
            screen.blit(shield_surf, (self.rect.centerx - shield_radius, self.rect.centery - shield_radius)) 