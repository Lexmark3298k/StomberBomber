"""
Clase Bala - Proyectiles del jugador - VERSION CORREGIDA
"""

import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y):
        super().__init__()
        
        # Tamaño de la bala
        self.image = pygame.Surface((8, 8))
        self.image.fill(YELLOW)
        pygame.draw.circle(self.image, ORANGE, (4, 4), 3)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Dirección y velocidad
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = 10
        self.damage = 15
        
        # Vida de la bala (frames)
        self.lifetime = 90
        
        print(f"Bala creada en ({x}, {y}) dirección: ({direction_x}, {direction_y})")  # Debug
        
    def update(self):
        """Actualizar posición de la bala"""
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        
        # Reducir vida útil
        self.lifetime -= 1
        
        # Si la bala sale de la pantalla o expira, eliminarla
        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.lifetime <= 0):
            self.kill()