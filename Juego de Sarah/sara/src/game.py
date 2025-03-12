import pygame
from player import Player
from level import Level
from ui import UI
from menu import Menu

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        self.score = 0
        self.level_number = 1
        self.high_score = 0
        self.sounds = {}
        
        # Cargar fuentes
        pygame.font.init()
        
        self.menu = Menu(self)
        self.ui = UI(self)
        self.level = None
        
        # Efectos visuales
        self.effects = []
        
        # Cargar o crear high score
        self.load_high_score()
    
    def load_high_score(self):
        try:
            with open('high_score.txt', 'r') as f:
                self.high_score = int(f.read())
        except:
            self.high_score = 0
    
    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open('high_score.txt', 'w') as f:
                    f.write(str(self.high_score))
            except:
                pass
    
    def load_resources(self):
        try:
            pygame.mixer.init()
            # Intentar cargar sonidos individualmente
            try:
                self.sounds['shoot'] = pygame.mixer.Sound('assets/sounds/shoot.mp3')
            except:
                print("No se pudo cargar shoot.wav")
            
            try:
                self.sounds['explosion'] = pygame.mixer.Sound('assets/sounds/explosion.mp3')
            except:
                print("No se pudo cargar explosion.wav")
            
            try:
                self.sounds['rescue'] = pygame.mixer.Sound('assets/sounds/rescue.mp3')
            except:
                print("No se pudo cargar rescue.wav")
            
            # Intentar cargar música
            try:
                pygame.mixer.music.load('assets/music/background.mp3')
                pygame.mixer.music.play(-1)
            except:
                print("No se pudo cargar la música de fondo")
                
        except:
            print("Sistema de audio no inicializado. El juego funcionará sin sonido.")
    
    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()
    
    def start_game(self):
        self.state = "GAME"
        self.score = 0
        self.level_number = 1
        self.create_level()
    
    def create_level(self):
        self.level = Level(self, self.level_number)
        # Mostrar mensaje de nivel
        self.ui.show_level_message()
    
    def next_level(self):
        self.level_number += 1
        # Bonus por completar nivel
        self.score += 5000 * self.level_number
        self.create_level()
    
    def add_effect(self, effect):
        self.effects.append(effect)
    
    def update_effects(self):
        for effect in self.effects[:]:
            effect.update()
            if effect.done:
                self.effects.remove(effect)
    
    def draw_effects(self):
        for effect in self.effects:
            effect.draw(self.screen)
    
    def game_over(self):
        self.save_high_score()
        self.state = "MENU"
        self.menu.show_game_over(self.score)
    
    def run(self):
        while self.running:
            self.handle_events()
            
            if self.state == "MENU":
                self.menu.update()
                self.menu.draw(self.screen)
            elif self.state == "GAME":
                self.level.update()
                self.level.draw(self.screen)
                self.ui.update()  # Actualizar UI
                self.update_effects()
                self.draw_effects()
                self.ui.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == "GAME":
                        self.game_over()
                    else:
                        self.running = False
                elif event.key == pygame.K_SPACE and self.state == "MENU":
                    self.start_game()