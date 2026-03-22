"""
Clase Láser - Para el sistema de trampas del Salón 3
"""

import pygame
import math
from settings import *

class Laser(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, laser_type="horizontal"):
        super().__init__()
        
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.laser_type = laser_type
        
        # Calcular longitud y ángulo
        self.length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        self.angle = math.degrees(math.atan2(y2 - y1, x2 - x1))
        
        # Crear superficie base
        self.image = pygame.Surface((int(self.length), 8), pygame.SRCALPHA)
        
        # Dibujar láser con gradiente
        for i in range(8):
            alpha = 255 - (abs(i - 4) * 30)
            color = (LASER_COLOR[0], LASER_COLOR[1], LASER_COLOR[2], alpha)
            pygame.draw.rect(self.image, color, (0, i, self.length, 1))
        
        # Rotar la superficie
        self.image = pygame.transform.rotate(self.image, -self.angle)
        
        self.rect = self.image.get_rect()
        self.rect.center = ((x1 + x2) // 2, (y1 + y2) // 2)
        
        # Estado del láser
        self.active = True
        self.damage = 100  # Daño letal
        self.pulse_timer = 0
        
    def update(self, is_active):
        """Actualizar estado del láser"""
        self.active = is_active
        
        if is_active:
            # Efecto de pulso cuando está activo
            self.pulse_timer += 0.2
            pulse = abs(math.sin(self.pulse_timer)) * 100
            self.image.set_alpha(150 + pulse)
        else:
            self.image.set_alpha(50)
            
    def check_collision(self, player_rect):
        """Verificar colisión con el jugador"""
        if not self.active:
            return False
        return self.rect.colliderect(player_rect)