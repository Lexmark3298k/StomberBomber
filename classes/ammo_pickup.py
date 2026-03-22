"""
Pickup de munición
"""

import pygame
import math
from settings import *

class AmmoPickup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        
        # Dibujar un casquillo de bala
        pygame.draw.rect(self.image, YELLOW, (5, 2, 5, 11))
        pygame.draw.circle(self.image, ORANGE, (7, 3), 3)
        pygame.draw.rect(self.image, GRAY, (6, 8, 3, 5))
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.original_y = y
        self.animation_offset = 0
        
    def update(self):
        """Animación flotante"""
        self.animation_offset += 0.1
        self.rect.y = self.original_y + math.sin(self.animation_offset) * 3