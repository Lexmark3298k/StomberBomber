"""
Clase base para todos los niveles - VERSION CORREGIDA
"""

import pygame
from settings import *

class LevelBase:
    def __init__(self, screen, player_data):
        self.screen = screen
        self.player_data = player_data
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Fuentes
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        
        # Variables de nivel
        self.completed = False
        self.level_name = ""
        
    def update(self):
        """Actualizar lógica del nivel - Sobrescribir"""
        pass
        
    def draw(self):
        """Dibujar el nivel"""
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_ui()
        
    def draw_ui(self):
        """Dibujar UI común"""
        # Barra de vida
        health_percentage = max(0, self.player_data["health"] / 100)
        pygame.draw.rect(self.screen, (64, 0, 0), (20, 20, 200, 25))
        
        if health_percentage > 0.6:
            health_color = GREEN
        elif health_percentage > 0.3:
            health_color = YELLOW
        else:
            health_color = RED
            
        pygame.draw.rect(self.screen, health_color, (20, 20, 200 * health_percentage, 25))
        
        # Texto de vida
        health_text = self.font.render(f"HP: {self.player_data['health']}", True, WHITE)
        self.screen.blit(health_text, (20, 48))
        
        # Llaves
        keys_text = self.font.render(f"KEYS: {self.player_data['keys']}/3", True, YELLOW)
        self.screen.blit(keys_text, (SCREEN_WIDTH - 120, 20))
        
        # Munición
        ammo = self.player_data.get("ammo", 30)
        ammo_text = self.font.render(f"AMMO: {ammo}", True, CYAN)
        self.screen.blit(ammo_text, (SCREEN_WIDTH - 120, 48))
        
        # Controles
        controls = pygame.font.Font(None, 16).render(
            "WASD: Mover | SPACE: Disparar | E: Interactuar", True, GRAY
        )
        self.screen.blit(controls, (20, SCREEN_HEIGHT - 25))
        
    def handle_bullet_collisions(self):
        """Manejar colisiones entre balas y enemigos - CORREGIDO"""
        for bullet in self.bullets:
            # Verificar colisión con cada enemigo
            for enemy in self.enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(bullet.damage)
                    bullet.kill()
                    break  # Una bala solo golpea a un enemigo