import pygame

class UI:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 72)
        
        self.level_message = None
        self.level_message_timer = 0
        self.level_message_duration = 120  # 2 segundos a 60 FPS
    
    def show_level_message(self):
        self.level_message = f"NIVEL {self.game.level_number}"
        self.level_message_timer = 0
    
    def update(self):
        if self.level_message:
            self.level_message_timer += 1
            if self.level_message_timer >= self.level_message_duration:
                self.level_message = None
    
    def draw(self, screen):
        if self.game.level is None:
            return
            
        # Mostrar puntaje
        score_text = self.font.render(f'Puntaje: {self.game.score}', True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # Mostrar vidas
        lives_text = self.font.render(f'Vidas: {self.game.level.player.lives}', True, (255, 255, 255))
        screen.blit(lives_text, (10, 50))
        
        # Mostrar nivel
        level_text = self.font.render(f'Nivel: {self.game.level_number}', True, (255, 255, 255))
        screen.blit(level_text, (10, 90))
        
        # Mostrar humanos restantes
        humans_text = self.small_font.render(f'Humanos: {len(self.game.level.humans)}', True, (255, 255, 0))
        screen.blit(humans_text, (10, 130))
        
        # Mostrar enemigos restantes
        enemies_text = self.small_font.render(f'Enemigos: {len(self.game.level.enemies)}', True, (255, 100, 100))
        screen.blit(enemies_text, (10, 160))
        
        # Mostrar mensaje de nivel si existe
        if self.level_message:
            alpha = 255
            if self.level_message_timer < 30:
                alpha = int(255 * (self.level_message_timer / 30))
            elif self.level_message_timer > self.level_message_duration - 30:
                alpha = int(255 * (1 - (self.level_message_timer - (self.level_message_duration - 30)) / 30))
            
            level_surf = self.big_font.render(self.level_message, True, (255, 255, 255))
            level_rect = level_surf.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            
            s = pygame.Surface(level_surf.get_size(), pygame.SRCALPHA)
            s.fill((0, 0, 0, 0))
            s.blit(level_surf, (0, 0))
            s.set_alpha(alpha)
            
            screen.blit(s, level_rect) 