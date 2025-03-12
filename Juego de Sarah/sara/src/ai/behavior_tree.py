import pygame
import random
import math

class Node:
    def __init__(self):
        self.status = "READY"
    
    def run(self):
        self.status = "RUNNING"
        return "RUNNING"

class Sequence(Node):
    def __init__(self, children=None):
        super().__init__()
        self.children = children or []

    def run(self):
        for child in self.children:
            status = child.run()
            if status != "SUCCESS":
                return status
        return "SUCCESS"

class Selector(Node):
    def __init__(self, children=None):
        super().__init__()
        self.children = children or []

    def run(self):
        for child in self.children:
            status = child.run()
            if status == "SUCCESS":
                return "SUCCESS"
        return "FAILURE"

# Nodos de comportamiento específicos
class CheckPlayerDistance(Node):
    def __init__(self, enemy):
        super().__init__()
        self.enemy = enemy
    
    def run(self):
        player_pos = self.enemy.game.level.player.rect.center
        distance = ((player_pos[0] - self.enemy.rect.centerx) ** 2 + 
                   (player_pos[1] - self.enemy.rect.centery) ** 2) ** 0.5
        self.enemy.distance_to_player = distance
        return "SUCCESS"

class ChasePlayer(Node):
    def __init__(self, enemy):
        super().__init__()
        self.enemy = enemy
    
    def run(self):
        player_pos = pygame.math.Vector2(self.enemy.game.level.player.rect.center)
        enemy_pos = pygame.math.Vector2(self.enemy.rect.center)
        direction = player_pos - enemy_pos
        if direction.length() > 0:
            direction = direction.normalize()
            self.enemy.pos += direction * self.enemy.speed
            self.enemy.rect.center = self.enemy.pos
        return "SUCCESS"

class Patrol(Node):
    def __init__(self, enemy):
        super().__init__()
        self.enemy = enemy
        self.patrol_time = 0
        self.direction_change_delay = 2000
    
    def run(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.patrol_time > self.direction_change_delay:
            self.patrol_time = current_time
            self.enemy.direction = pygame.math.Vector2(
                random.uniform(-1, 1),
                random.uniform(-1, 1)
            ).normalize()
        
        self.enemy.pos += self.enemy.direction * self.enemy.speed
        self.enemy.rect.center = self.enemy.pos
        self.enemy.rect.clamp_ip(pygame.display.get_surface().get_rect())
        return "SUCCESS" 