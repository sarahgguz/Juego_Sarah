import pygame
import random
from ai.behavior_tree import Sequence, Selector, CheckPlayerDistance, Patrol
from utils.create_sprites import create_brain_sprite

class Brain(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__()
        self.game = game
        self.image = create_brain_sprite()
        self.rect = self.image.get_rect(center=pos)
        self.speed = 0.8  # Muy lento
        self.health = 2
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(1, 0)
        self.distance_to_player = float('inf')
        
        # Temporizador para generar enemigos
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 8000  # 8 segundos entre spawns
        
        self.setup_behavior_tree()
    
    def setup_behavior_tree(self):
        # El Brain principalmente patrulla y ocasionalmente genera enemigos
        self.bt = Sequence([
            CheckPlayerDistance(self),
            Patrol(self)
        ])
    
    def update(self):
        self.bt.run()
        
        # Generar un enemigo cada cierto tiempo
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_delay:
            self.spawn_timer = current_time
            self.spawn_grunt()
    
    def spawn_grunt(self):
        # Solo generar si no hay demasiados enemigos
        if len(self.game.level.enemies) < 10:
            from enemy.grunt import Grunt
            
            # Generar cerca del Brain
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            pos = (self.rect.centerx + offset_x, self.rect.centery + offset_y)
            
            # Asegurarse de que esté dentro de la pantalla
            screen_rect = pygame.display.get_surface().get_rect()
            pos = (
                max(20, min(screen_rect.width - 20, pos[0])),
                max(20, min(screen_rect.height - 20, pos[1]))
            )
            
            grunt = Grunt(self.game, pos)
            self.game.level.enemies.add(grunt)
            self.game.level.all_sprites.add(grunt) 