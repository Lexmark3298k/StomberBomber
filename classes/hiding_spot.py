"""
Clase Escondite - Para el sistema de sigilo
"""

import pygame
import math
from settings import *

class HidingSpot(pygame.sprite.Sprite):
    def __init__(self, x, y, spot_type="fossil"):
        super().__init__()
        
        self.spot_type = spot_type
        self.is_occupied = False
        
        # Crear sprite según tipo
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10), pygame.SRCALPHA)
        
        if spot_type == "fossil":
            # Dibujar un fósil
            pygame.draw.rect(self.image, (139, 69, 19), (5, 15, 30, 20))
            pygame.draw.circle(self.image, (139, 69, 19), (20, 10), 8)
            pygame.draw.line(self.image, (100, 50, 10), (10, 25), (30, 25), 2)
            self.color = HIDING_COLOR
        elif spot_type == "exhibit":
            # Dibujar una vitrina
            pygame.draw.rect(self.image, (100, 100, 100), (5, 5, 30, 35), 2)
            pygame.draw.circle(self.image, CYAN, (20, 20), 5)
        else:  # bush
            # Dibujar arbusto
            pygame.draw.ellipse(self.image, DARK_GREEN, (5, 10, 30, 25))
            pygame.draw.ellipse(self.image, GREEN, (2, 5, 15, 20))
            pygame.draw.ellipse(self.image, GREEN, (23, 5, 15, 20))
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animación de brillo cuando está cerca
        self.glow_timer = 0
        self.glow_alpha = 0
        
    def update(self, player_distance=0):
        """Actualizar animación del escondite"""
        # Brillo cuando el jugador está cerca
        if player_distance < 50 and not self.is_occupied:
            self.glow_timer += 0.2
            self.glow_alpha = 100 + math.sin(self.glow_timer) * 50
        else:
            self.glow_alpha = max(0, self.glow_alpha - 5)
            
    def interact(self, player):
        """Interactuar con el escondite"""
        if not self.is_occupied:
            self.is_occupied = True
            player.hide(self.rect.centerx, self.rect.centery, self)
            return True
        return False
        
    def get_out(self):
        """Salir del escondite"""
        self.is_occupied = False