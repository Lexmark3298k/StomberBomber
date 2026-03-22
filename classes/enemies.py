"""
Clases de enemigos - Agregando Raptor Fantasma
"""

import pygame
import math
import random
from settings import *

class ChainsawDino(pygame.sprite.Sprite):
    """Dinosaurio con motosierra - Persigue al jugador"""
    def __init__(self, x, y):
        # CORREGIDO: Llamar a super().__init__() correctamente
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((45, 45))
        self.image.fill(RED)
        
        # Dibujar detalles simples
        pygame.draw.circle(self.image, WHITE, (10, 15), 5)
        pygame.draw.circle(self.image, WHITE, (35, 15), 5)
        pygame.draw.circle(self.image, BLACK, (10, 15), 2)
        pygame.draw.circle(self.image, BLACK, (35, 15), 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Estadísticas
        self.health = 30
        self.max_health = 30
        self.speed = 2.5
        self.alive = True
        self.damage = 10
        
        # Cooldown de ataque
        self.attack_cooldown = 0
        self.attack_cooldown_max = 30
        
    def update(self, player):
        """Perseguir al jugador"""
        if not self.alive:
            return
            
        # Actualizar cooldown de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Calcular dirección hacia el jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        # Moverse hacia el jugador si está a más de 5 píxeles
        if distance > 5 and distance < 500:
            if distance > 0:
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed
                
        # Limitar al borde de la pantalla
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
    def take_damage(self, amount):
        """Recibir daño"""
        self.health -= amount
        print(f"Dinosaurio recibe {amount} daño. Vida restante: {self.health}")
        
        # Efecto visual de daño
        self.image.fill(ORANGE)
        # Restaurar color después de un momento (esto se manejaría mejor con un timer)
        
        if self.health <= 0:
            self.alive = False
            print("Dinosaurio derrotado!")
            return True
        return False

class RaptorFantasma(pygame.sprite.Sprite):
    """Raptor invisible - Sistema de sigilo"""
    def __init__(self, x, y, patrol_points):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10), pygame.SRCALPHA)
        
        # Dibujar raptor fantasmal
        pygame.draw.ellipse(self.image, RAPTOR_COLOR, (5, 10, 30, 25))
        pygame.draw.circle(self.image, WHITE, (12, 18), 4)
        pygame.draw.circle(self.image, WHITE, (28, 18), 4)
        pygame.draw.circle(self.image, BLACK, (12, 18), 2)
        pygame.draw.circle(self.image, BLACK, (28, 18), 2)
        pygame.draw.polygon(self.image, RAPTOR_COLOR, [(20, 25), (15, 35), (25, 35)])
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Estado de la IA
        self.state = "patrol"  # patrol, chase, confused, searching
        self.patrol_points = patrol_points
        self.current_target = 0
        self.speed = PATROL_SPEED
        self.chase_speed = CHASE_SPEED
        
        # Sistema de visión
        self.vision_range = VISION_RANGE
        self.vision_angle = VISION_ANGLE
        self.alert_level = 0
        self.alert_decay = 1
        
        # Transparencia (fantasma)
        self.alpha = 100
        self.image.set_alpha(self.alpha)
        
        # Dirección actual
        self.direction = 0  # 0: derecha, 1: izquierda, etc.
        self.facing_angle = 0
        
        # Temporizadores
        self.confused_timer = 0
        self.last_known_position = None
        self.search_position = None
        self.search_timer = 0
        
        # Sonidos de alerta (simulados)
        self.alert_sound_timer = 0
        
    def update(self, player, obstacles=None):
        """Actualizar comportamiento del raptor"""
        if obstacles is None:
            obstacles = []
            
        # Verificar si ve al jugador
        can_see_player = self.check_line_of_sight(player, obstacles)
        
        # Decaer alert level
        if self.alert_level > 0 and self.state != "chase":
            self.alert_level -= self.alert_decay
            
        # Máquina de estados
        if self.state == "patrol":
            self.patrol_behavior()
            
            if can_see_player and not player.is_hiding:
                self.state = "chase"
                self.speed = self.chase_speed
                self.alert_level = 100
                self.alpha = 255
                self.image.set_alpha(self.alpha)
                self.alert_sound_timer = 10
                
        elif self.state == "chase":
            self.chase_behavior(player)
            
            # Si pierde de vista al jugador
            if not can_see_player or player.is_hiding:
                self.alert_level -= 2
                if self.alert_level <= 0:
                    self.state = "searching"
                    self.search_position = self.last_known_position
                    self.search_timer = 120  # Buscar por 2 segundos
                    self.speed = PATROL_SPEED
                    
        elif self.state == "searching":
            self.search_behavior()
            
            self.search_timer -= 1
            if self.search_timer <= 0:
                self.state = "patrol"
                self.alpha = 100
                self.image.set_alpha(self.alpha)
                self.speed = PATROL_SPEED
                self.last_known_position = None
                
        elif self.state == "confused":
            self.confused_behavior()
            
        # Actualizar ángulo de visión
        if self.rect.centerx > 0:
            self.facing_angle = math.degrees(math.atan2(
                player.rect.centery - self.rect.centery,
                player.rect.centerx - self.rect.centerx
            ))
            
        # Limitar movimiento
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
        # Actualizar sonido de alerta
        if self.alert_sound_timer > 0:
            self.alert_sound_timer -= 1
            
    def patrol_behavior(self):
        """Comportamiento de patrulla"""
        target_x, target_y = self.patrol_points[self.current_target]
        self.move_towards(target_x, target_y)
        
        if self.reached_position(target_x, target_y):
            self.current_target = (self.current_target + 1) % len(self.patrol_points)
            
    def chase_behavior(self, player):
        """Perseguir al jugador"""
        self.last_known_position = (player.rect.centerx, player.rect.centery)
        self.move_towards(player.rect.centerx, player.rect.centery)
        
    def search_behavior(self):
        """Buscar al jugador en la última posición conocida"""
        if self.search_position:
            self.move_towards(self.search_position[0], self.search_position[1])
            if self.reached_position(self.search_position[0], self.search_position[1]):
                self.search_position = None
                
    def confused_behavior(self):
        """Comportamiento confundido - gira en círculo"""
        # Rotación simple
        self.direction = (self.direction + 1) % 360
        angle_rad = math.radians(self.direction)
        self.rect.x += math.cos(angle_rad) * 1
        self.rect.y += math.sin(angle_rad) * 1
        
    def move_towards(self, target_x, target_y):
        """Moverse hacia un punto"""
        dx = target_x - self.rect.centerx
        dy = target_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed
            
    def reached_position(self, x, y, tolerance=20):
        """Verificar si llegó a la posición"""
        return abs(self.rect.centerx - x) < tolerance and abs(self.rect.centery - y) < tolerance
        
    def check_line_of_sight(self, player, obstacles):
        """Verificar línea de visión con el jugador"""
        # Si el jugador está escondido, no se le ve
        if player.is_hiding:
            return False
            
        # Calcular vector hacia el jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        # Verificar distancia
        if distance > self.vision_range:
            return False
        
        # Verificar ángulo de visión (cono)
        angle_to_player = math.degrees(math.atan2(dy, dx))
        angle_diff = abs(angle_to_player - self.facing_angle)
        
        # Normalizar ángulo
        if angle_diff > 180:
            angle_diff = 360 - angle_diff
            
        if angle_diff > self.vision_angle / 2:
            return False
        
        # Raycasting simple para obstáculos
        return not self.has_obstacle_between(player, obstacles)
        
    def has_obstacle_between(self, player, obstacles):
        """Verificar si hay obstáculos entre el raptor y el jugador"""
        # Implementación simplificada
        # En un juego real, usarías raycasting más preciso
        step_x = (player.rect.centerx - self.rect.centerx) / 20
        step_y = (player.rect.centery - self.rect.centery) / 20
        
        x = self.rect.centerx
        y = self.rect.centery
        
        for _ in range(20):
            x += step_x
            y += step_y
            
            for obs in obstacles:
                if isinstance(obs, pygame.Rect) and obs.collidepoint(x, y):
                    return True
                    
        return False