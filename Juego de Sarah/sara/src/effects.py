import pygame
import random
import math

class Explosion:
    def __init__(self, pos, color=(255, 200, 0), particles=20):
        self.pos = pos
        self.particles = []
        self.done = False
        self.lifetime = 30
        self.timer = 0
        
        for _ in range(particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            size = random.randint(2, 5)
            self.particles.append({
                'pos': list(pos),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'size': size,
                'color': color,
                'alpha': 255
            })
    
    def update(self):
        self.timer += 1
        if self.timer >= self.lifetime:
            self.done = True
            
        for p in self.particles:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['alpha'] = max(0, 255 * (1 - self.timer / self.lifetime))
    
    def draw(self, screen):
        for p in self.particles:
            color = p['color']
            alpha = int(p['alpha'])
            s = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, alpha), (p['size'], p['size']), p['size'])
            screen.blit(s, (p['pos'][0] - p['size'], p['pos'][1] - p['size']))

class TextEffect:
    def __init__(self, text, pos, color=(255, 255, 255), size=20, duration=60):
        self.font = pygame.font.Font(None, size)
        self.text = self.font.render(text, True, color)
        self.pos = list(pos)
        self.vel = [0, -1]  # Movimiento hacia arriba
        self.alpha = 255
        self.duration = duration
        self.timer = 0
        self.done = False
    
    def update(self):
        self.timer += 1
        if self.timer >= self.duration:
            self.done = True
        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.alpha = max(0, 255 * (1 - self.timer / self.duration))
    
    def draw(self, screen):
        s = pygame.Surface(self.text.get_size(), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        s.blit(self.text, (0, 0))
        s.set_alpha(self.alpha)
        screen.blit(s, self.pos) 