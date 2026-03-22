"""
Clase del Jugador - Stomber Bomber
Con sistema de disparos y sigilo
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
        self.facing_right = True
        
        # Sistema de sigilo (NUEVO)
        self.is_hiding = False
        self.current_hiding_spot = None
        self.hide_position = None
        self.in_safe_zone = False
        
        # Sistema de disparo
        self.shoot_timer = 0
        self.shoot_cooldown = 15
        self.last_shot_direction = (1, 0)
        
        # Referencia a los datos del jugador
        self.player_data = player_data
        
    def handle_input(self, keys):
        """Manejar entrada del teclado - RETORNA LA BALA SI DISPARA"""
        
        # Si está escondido, no se mueve ni dispara
        if self.is_hiding:
            return None
            
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
        
        # Disparo
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0 and self.ammo > 0:
            return self.shoot()
            
        return None
        
    def shoot(self):
        """Disparar arma - crea y retorna la bala"""
        self.shoot_timer = self.shoot_cooldown
        self.ammo -= 1
        self.player_data["ammo"] = self.ammo
        
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
        # Si está escondido, no recibe daño
        if self.invincible_timer <= 0 and not self.is_hiding:
            self.health -= amount
            self.invincible_timer = self.invincible_duration
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
        
    # ========== MÉTODOS DE SIGILO ==========
    
    def hide(self, x, y, hiding_spot):
        """Esconderse en un spot"""
        self.is_hiding = True
        self.current_hiding_spot = hiding_spot
        self.hide_position = (x, y)
        self.rect.centerx = x
        self.rect.centery = y
        # Cambiar apariencia para indicar que está escondido
        self.image.fill((0, 0, 100))
        print("Jugador escondido!")
        
    def unhide(self):
        """Salir del escondite"""
        self.is_hiding = False
        if self.current_hiding_spot:
            self.current_hiding_spot.get_out()
            self.current_hiding_spot = None
        self.hide_position = None
        self.image.fill(BLUE)