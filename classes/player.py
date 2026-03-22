"""
Clase del Jugador - Stomber Bomber
Con sistema de disparos - VERSION CORREGIDA
"""

import pygame
import math
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, player_data):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Datos del jugador
        self.health = player_data["health"]
        self.max_health = 100
        self.keys = player_data["keys"]
        self.ammo = player_data.get("ammo", 30)
        self.max_ammo = 99
        
        # Estado del jugador
        self.velocity_x = 0
        self.velocity_y = 0
        self.invincible_timer = 0
        self.invincible_duration = 60
        self.is_hiding = False
        self.facing_right = True
        
        # Sistema de disparo - CORREGIDO
        self.shoot_timer = 0
        self.shoot_cooldown = 15  # frames entre disparos
        
        # Dirección del último disparo (por defecto derecha)
        self.last_shot_direction = (1, 0)
        
        # Referencia a los datos del jugador
        self.player_data = player_data
        
    def handle_input(self, keys):
        """Manejar entrada del teclado - RETORNA LA BALA SI DISPARA"""
        
        # Actualizar timers
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
            
        if self.shoot_timer > 0:
            self.shoot_timer -= 1
            
        # Movimiento
        self.velocity_x = 0
        self.velocity_y = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
            self.last_shot_direction = (-1, 0)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
            self.last_shot_direction = (1, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity_y = -PLAYER_SPEED
            self.last_shot_direction = (0, -1)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity_y = PLAYER_SPEED
            self.last_shot_direction = (0, 1)
            
        # Aplicar movimiento
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Limitar al borde de la pantalla
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, SCREEN_HEIGHT - self.rect.height))
        
        # Disparo - CORREGIDO: retorna la bala si se dispara
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0 and self.ammo > 0:
            return self.shoot()
            
        return None
        
    def shoot(self):
        """Disparar arma - crea y retorna la bala"""
        self.shoot_timer = self.shoot_cooldown
        self.ammo -= 1
        
        # Actualizar datos
        self.player_data["ammo"] = self.ammo
        
        # Crear bala
        from classes.bullet import Bullet
        bullet = Bullet(
            self.rect.centerx, 
            self.rect.centery,
            self.last_shot_direction[0],
            self.last_shot_direction[1]
        )
        return bullet
        
    def take_damage(self, amount):
        """Recibir daño"""
        if self.invincible_timer <= 0 and not self.is_hiding:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
            # Actualizar datos
            self.player_data["health"] = self.health
            
            # Efecto visual de daño
            self.image.fill(RED)
            pygame.time.wait(50)
            self.image.fill(BLUE)
            
            return True
        return False
        
    def add_ammo(self, amount):
        """Añadir munición"""
        self.ammo = min(self.max_ammo, self.ammo + amount)
        self.player_data["ammo"] = self.ammo
        
    def add_key(self):
        """Añadir una llave"""
        self.keys += 1
        self.player_data["keys"] = self.keys