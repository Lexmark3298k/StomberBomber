"""
Clases de enemigos
"""

import pygame
import math
import random
from settings import *

class ChainsawDino(pygame.sprite.Sprite):
    """Dinosaurio con motosierra - Salón 1"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 5, TILE_SIZE - 5))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.health = 30
        self.speed = 2
        self.alive = True
        self.damage = 10
        
    def update(self, player):
        """Perseguir al jugador"""
        if not self.alive:
            return
            
        # Movimiento hacia el jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
            
    def take_damage(self, amount):
        """Recibir daño"""
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            
class RaptorFantasma(pygame.sprite.Sprite):
    """Raptor invisible - Salón 2 (Sigilo)"""
    def __init__(self, x, y, patrol_points):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(RAPTOR_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Estado
        self.state = "patrol"  # patrol, chase, confused
        self.patrol_points = patrol_points
        self.current_target = 0
        self.speed = PATROL_SPEED
        self.chase_speed = CHASE_SPEED
        
        # Visión
        self.vision_range = VISION_RANGE
        self.vision_angle = VISION_ANGLE
        self.alert_level = 0
        
        # Transparencia
        self.alpha = 128
        self.image.set_alpha(self.alpha)
        
        # Temporizadores
        self.confused_timer = 0
        self.last_known_position = None
        self.facing_angle = 0
        
    def update(self, player, obstacles):
        """Actualizar comportamiento"""
        # Aquí iría toda la lógica de sigilo explicada anteriormente
        # (Por brevedad, se simplifica)
        
        # Movimiento básico de patrulla
        if self.state == "patrol":
            target_x, target_y = self.patrol_points[self.current_target]
            self.move_towards(target_x, target_y)
            
            if self.reached_position(target_x, target_y):
                self.current_target = (self.current_target + 1) % len(self.patrol_points)
                
    def move_towards(self, target_x, target_y):
        """Moverse hacia un punto"""
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
            
    def reached_position(self, x, y, tolerance=10):
        """Verificar si llegó a la posición"""
        return abs(self.rect.centerx - x) < tolerance and abs(self.rect.centery - y) < tolerance