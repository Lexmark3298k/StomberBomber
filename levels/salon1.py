"""
Salón 1 - Carnicería Cretácica
Mecánica: Combate directo contra dinosaurios con motosierra
"""

import pygame
import random
from levels.level_base import LevelBase
from classes.player import Player
from classes.enemies import ChainsawDino
from settings import *

class Salon1(LevelBase):
    def __init__(self, screen, player_data):
        super().__init__(screen, player_data)
        
        # Crear jugador
        self.player = Player(100, 300, player_data)
        self.all_sprites.add(self.player)
        
        # Crear enemigos (dinosaurios con motosierra)
        self.enemies = pygame.sprite.Group()
        enemy_positions = [(400, 200), (600, 300), (350, 450), (550, 500)]
        
        for x, y in enemy_positions:
            dino = ChainsawDino(x, y)
            self.enemies.add(dino)
            self.all_sprites.add(dino)
            
        # Llave (aparece después de derrotar a todos)
        self.key = None
        self.key_position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.key_found = False
        
        # Variables de nivel
        self.completed = False
        self.enemies_defeated = 0
        self.total_enemies = len(self.enemies)
        
    def update(self):
        """Actualizar lógica del nivel"""
        # Manejar entrada del jugador
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys)
        
        # Actualizar enemigos
        for enemy in self.enemies:
            enemy.update(self.player)
            
            # Verificar colisión con jugador
            if self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(10)
                # Retroceder al jugador
                self.player.knockback(enemy.rect.center)
                
        # Verificar enemigos derrotados
        for enemy in self.enemies:
            if enemy.health <= 0 and enemy.alive:
                enemy.alive = False
                self.enemies_defeated += 1
                enemy.kill()
                
        # Crear llave cuando todos los enemigos están muertos
        if self.enemies_defeated >= self.total_enemies and not self.key_found and not self.key:
            self.key = Key(self.key_position[0], self.key_position[1])
            self.all_sprites.add(self.key)
            
        # Recoger llave
        if self.key and not self.key_found:
            if self.player.rect.colliderect(self.key.rect):
                if keys[pygame.K_e]:
                    self.key_found = True
                    self.player_data["keys"] += 1
                    if self.key_sound:
                        self.key_sound.play()
                    self.key.kill()
                    
        # Verificar si puede avanzar
        if self.key_found:
            # Puerta de salida
            exit_door = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - 25, 50, 50)
            if self.player.rect.colliderect(exit_door) and keys[pygame.K_e]:
                return "next_level"
                
        # Verificar si el jugador murió
        if self.player_data["health"] <= 0:
            return "game_over"
            
        return None
        
    def draw(self):
        """Dibujar el nivel"""
        super().draw()
        
        # Dibujar enemigos muertos (sangre simulada - estilo DOS)
        # (Opcional: dibujar manchas rojas donde murieron)
        
        # Dibujar puerta de salida
        if self.key_found:
            pygame.draw.rect(self.screen, GREEN, (SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - 25, 50, 50))
            door_text = pygame.font.Font(None, 16).render("EXIT", True, WHITE)
            self.screen.blit(door_text, (SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2 - 10))
            
        # Mostrar contador de enemigos
        enemies_text = self.font.render(f"Enemigos: {self.enemies_defeated}/{self.total_enemies}", True, RED)
        self.screen.blit(enemies_text, (SCREEN_WIDTH // 2 - 80, 20))

class Key(pygame.sprite.Sprite):
    """Llave para avanzar de nivel"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.animation_offset = 0
        
    def update(self):
        """Animación flotante"""
        self.animation_offset += 0.1
        self.rect.y += math.sin(self.animation_offset) * 0.5