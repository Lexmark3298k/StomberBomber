"""
Clase del Jugador - Stomber Bomber
"""

import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_data):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Datos del jugador
        self.health = player_data["health"]
        self.keys = player_data["keys"]
        self.ammo = player_data.get("ammo", 30)
        
        # Estado del jugador
        self.velocity_x = 0
        self.velocity_y = 0
        self.invincible_timer = 0
        self.is_hiding = False
        self.in_safe_zone = False
        self.facing_right = True
        
        # Sistema de disparo
        self.shoot_timer = 0
        self.shoot_cooldown = PLAYER_SHOT_COOLDOWN
        
    def handle_input(self, keys):
        """Manejar entrada del teclado"""
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            
        # Movimiento
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -PLAYER_SPEED
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = PLAYER_SPEED
            
        # Disparo (espacio)
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot()
            
        # Actualizar timers
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
            
        # Aplicar movimiento
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Limitar al borde de la pantalla
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
    def shoot(self):
        """Disparar arma"""
        if self.ammo > 0:
            self.shoot_timer = self.shoot_cooldown
            self.ammo -= 1
            # Aquí se crearía el proyectil
            return True
        return False
        
    def take_damage(self, amount):
        """Recibir daño"""
        if self.invincible_timer <= 0 and not self.is_hiding:
            self.health -= amount
            self.invincible_timer = 30  # Invulnerabilidad temporal
            return True
        return False
        
    def knockback(self, source_pos):
        """Empujar al jugador cuando recibe daño"""
        dx = self.rect.centerx - source_pos[0]
        dy = self.rect.centery - source_pos[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.rect.x += (dx / distance) * 30
            self.rect.y += (dy / distance) * 30
            
    def hide(self, spot_position):
        """Esconderse en un spot"""
        self.is_hiding = True
        self.rect.center = spot_position
        
    def die(self):
        """Muerte instantánea"""
        self.health = 0
        
    def heal(self, amount):
        """Curar al jugador"""
        self.health = min(100, self.health + amount)