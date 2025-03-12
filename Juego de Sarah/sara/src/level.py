import pygame
from player import Player
from enemy.grunt import Grunt
from enemy.hulk import Hulk
from enemy.brain import Brain
from human import Human
import random
from powerup import PowerUp
from effects import Explosion, TextEffect

class Level:
    def __init__(self, game, level_number):
        self.game = game
        self.level_number = level_number
        
        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.humans = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        
        # Crear jugador
        self.player = Player(self.game, (400, 300))
        self.all_sprites.add(self.player)
        
        # Crear enemigos y humanos
        self.spawn_enemies()
        self.spawn_humans()
        
        # Timer para spawn progresivo de enemigos
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_delay = 5000  # 5 segundos entre spawns
        
        # Probabilidad de spawn de power-up
        self.powerup_chance = 0.3  # 30% de probabilidad
    
    def spawn_enemies(self):
        # Número base de enemigos según el nivel
        num_grunts = min(2 + self.level_number // 2, 5)  # Máximo 5 grunts
        num_hulks = min(self.level_number // 3, 2)       # Máximo 2 hulks
        num_brains = min(self.level_number // 4, 1)      # Máximo 1 brain
        
        # Spawn inicial de enemigos
        for _ in range(num_grunts):
            self.spawn_enemy('grunt')
        for _ in range(num_hulks):
            self.spawn_enemy('hulk')
        for _ in range(num_brains):
            self.spawn_enemy('brain')
    
    def spawn_enemy(self, enemy_type):
        # Spawn enemigos lejos del jugador
        while True:
            pos = (random.randint(50, 750), random.randint(50, 550))
            player_dist = ((pos[0] - self.player.rect.centerx) ** 2 + 
                         (pos[1] - self.player.rect.centery) ** 2) ** 0.5
            if player_dist > 200:  # Mínimo 200 píxeles del jugador
                break
        
        if enemy_type == 'grunt':
            enemy = Grunt(self.game, pos)
        elif enemy_type == 'hulk':
            enemy = Hulk(self.game, pos)
        elif enemy_type == 'brain':
            enemy = Brain(self.game, pos)
        else:
            enemy = Grunt(self.game, pos)  # Por defecto
        
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
    
    def spawn_humans(self):
        num_humans = 3 + self.level_number  # Más humanos en niveles superiores
        for _ in range(num_humans):
            pos = (random.randint(50, 750), random.randint(50, 550))
            human = Human(self.game, pos)
            self.humans.add(human)
            self.all_sprites.add(human)
    
    def update(self):
        self.all_sprites.update()
        self.projectiles.update()
        self.powerups.update()
        self.check_collisions()
        
        # Spawn progresivo de enemigos
        current_time = pygame.time.get_ticks()
        if (current_time - self.spawn_timer > self.spawn_delay and 
            len(self.enemies) < 5 + self.level_number):
            self.spawn_timer = current_time
            self.spawn_enemy('grunt')
        
        # Verificar victoria del nivel
        if not self.humans and not self.enemies:
            self.game.next_level()
    
    def draw(self, screen):
        # Fondo con estrellas
        screen.fill((0, 0, 0))
        
        # Dibujar estrellas (solo una vez al crear el nivel)
        if not hasattr(self, 'background'):
            self.background = pygame.Surface(screen.get_size())
            self.background.fill((0, 0, 0))
            
            # Estrellas pequeñas
            for _ in range(100):
                x = random.randint(0, screen.get_width())
                y = random.randint(0, screen.get_height())
                radius = random.randint(1, 2)
                brightness = random.randint(100, 255)
                color = (brightness, brightness, brightness)
                pygame.draw.circle(self.background, color, (x, y), radius)
            
            # Estrellas medianas
            for _ in range(30):
                x = random.randint(0, screen.get_width())
                y = random.randint(0, screen.get_height())
                radius = random.randint(2, 3)
                brightness = random.randint(150, 255)
                color = (brightness, brightness, brightness)
                pygame.draw.circle(self.background, color, (x, y), radius)
            
            # Nebulosas
            for _ in range(5):
                x = random.randint(0, screen.get_width())
                y = random.randint(0, screen.get_height())
                width = random.randint(100, 200)
                height = random.randint(100, 200)
                color_r = random.randint(0, 30)
                color_g = random.randint(0, 30)
                color_b = random.randint(0, 30)
                
                nebula_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                pygame.draw.ellipse(nebula_surf, (color_r, color_g, color_b, 50), (0, 0, width, height))
                self.background.blit(nebula_surf, (x, y))
        
        # Dibujar fondo
        screen.blit(self.background, (0, 0))
        
        # Dibujar sprites
        self.all_sprites.draw(screen)
        self.projectiles.draw(screen)
        self.powerups.draw(screen)
    
    def check_collisions(self):
        # Proyectil - Enemigo
        hits = pygame.sprite.groupcollide(self.projectiles, self.enemies, True, True)
        for proj, enemies in hits.items():
            for enemy in enemies:
                self.game.score += 100 * self.level_number
                self.game.add_effect(Explosion(enemy.rect.center))
                self.game.add_effect(TextEffect(f"+{100 * self.level_number}", enemy.rect.center))
                
                # Posibilidad de soltar power-up
                if random.random() < self.powerup_chance:
                    powerup_type = random.choice(["health", "speed", "shield", "rapid"])
                    powerup = PowerUp(self.game, enemy.rect.center, powerup_type)
                    self.powerups.add(powerup)
        
        # Jugador - Enemigo
        if not self.player.invincible:
            hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if hits:
                if self.player.take_damage():
                    self.game.add_effect(Explosion(self.player.rect.center, color=(0, 100, 255)))
        
        # Jugador - Humano
        rescued = pygame.sprite.spritecollide(self.player, self.humans, True)
        for human in rescued:
            points = 1000 * self.level_number
            self.game.score += points
            self.game.add_effect(TextEffect(f"+{points}", human.rect.center, (255, 255, 0)))
        
        # Jugador - PowerUp
        powerup_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for powerup in powerup_hits:
            powerup.apply(self.player) 