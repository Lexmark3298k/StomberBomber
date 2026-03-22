"""
Clase base para todos los niveles
"""

import pygame
from settings import *

class LevelBase:
    def __init__(self, screen, player_data):
        self.screen = screen
        self.player_data = player_data
        self.all_sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(None, 24)
        
        # Cargar sonidos (opcional)
        try:
            self.key_sound = pygame.mixer.Sound("assets/sounds/key_pickup.wav")
        except:
            self.key_sound = None
            
    def update(self):
        """Actualizar lógica del nivel - Sobrescribir en cada nivel"""
        pass
        
    def draw(self):
        """Dibujar el nivel - Sobrescribir en cada nivel"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_ui()
        
    def draw_ui(self):
        """Dibujar UI común (vida, llaves, etc.)"""
        # Barra de vida
        health_percentage = self.player_data["health"] / 100
        pygame.draw.rect(self.screen, HEALTH_BG_COLOR, (20, 20, 200, 20))
        pygame.draw.rect(self.screen, HEALTH_BAR_COLOR, (20, 20, 200 * health_percentage, 20))
        
        # Texto de vida
        health_text = self.font.render(f"HP: {self.player_data['health']}", True, WHITE)
        self.screen.blit(health_text, (20, 45))
        
        # Llaves
        keys_text = self.font.render(f"KEYS: {self.player_data['keys']}/3", True, YELLOW)
        self.screen.blit(keys_text, (SCREEN_WIDTH - 120, 20))
        
        # Instrucciones básicas
        controls_text = pygame.font.Font(None, 16).render("WASD: Mover | E: Interactuar | R: Reiniciar", True, GRAY)
        self.screen.blit(controls_text, (20, SCREEN_HEIGHT - 30))