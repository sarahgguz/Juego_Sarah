import pygame

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 74)
        self.medium_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.game_over = False
        self.final_score = 0
        
        # Colores
        self.title_color = (255, 255, 0)
        self.text_color = (255, 255, 255)
        self.highlight_color = (0, 255, 255)
    
    def update(self):
        pass
    
    def draw(self, screen):
        screen.fill((0, 0, 0))
        
        # Título
        title = self.font.render('ROBOTRON 2084', True, self.title_color)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150))
        screen.blit(title, title_rect)
        
        if self.game_over:
            # Mensaje de Game Over
            game_over_text = self.medium_font.render('GAME OVER', True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, 250))
            screen.blit(game_over_text, game_over_rect)
            
            # Puntaje final
            score_text = self.small_font.render(f'Puntaje final: {self.final_score}', True, self.text_color)
            score_rect = score_text.get_rect(center=(screen.get_width() // 2, 320))
            screen.blit(score_text, score_rect)
        
        # High score
        high_score_text = self.small_font.render(f'High Score: {self.game.high_score}', True, self.highlight_color)
        high_score_rect = high_score_text.get_rect(center=(screen.get_width() // 2, 380))
        screen.blit(high_score_text, high_score_rect)
        
        # Instrucciones
        instructions = [
            "Controles:",
            "Flechas - Mover",
            "Mouse - Apuntar",
            "Clic izquierdo - Disparar",
            "ESC - Salir",
            "",
            "Presiona ESPACIO para comenzar"
        ]
        
        y = 430
        for i, line in enumerate(instructions):
            color = self.highlight_color if i == len(instructions) - 1 else self.text_color
            text = self.small_font.render(line, True, color)
            rect = text.get_rect(center=(screen.get_width() // 2, y))
            screen.blit(text, rect)
            y += 30
    
    def show_game_over(self, score):
        self.game_over = True
        self.final_score = score 