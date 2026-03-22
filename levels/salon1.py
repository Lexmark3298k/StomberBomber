"""
Salón 1 - Carnicería Cretácica - VERSION CORREGIDA
"""

import pygame
import math
from levels.level_base import LevelBase
from classes.player import Player
from classes.enemies import ChainsawDino
from settings import *

class Salon1(LevelBase):
    def __init__(self, screen, player_data):
        super().__init__(screen, player_data)
        
        self.level_name = "CARNICERIA CRETACICA"
        
        # Crear jugador
        self.player = Player(100, 300, player_data)
        self.all_sprites.add(self.player)
        
        # Crear enemigos (3 enemigos para probar)
        enemy_positions = [
            (400, 200),
            (600, 300),
            (350, 450)
        ]
        
        # CORREGIDO: Crear enemigos y agregarlos correctamente
        for x, y in enemy_positions:
            dino = ChainsawDino(x, y)
            self.enemies.add(dino)      # Agregar al grupo de enemigos
            self.all_sprites.add(dino)  # Agregar al grupo general
        
        # Variables de nivel
        self.total_enemies = len(self.enemies)
        self.enemies_defeated = 0
        self.key = None
        self.key_found = False
        self.exit_door = None
        
        print(f"Salón 1 iniciado. Enemigos: {self.total_enemies}")
        
    def update(self):
        """Actualizar lógica del nivel"""
        keys = pygame.key.get_pressed()
        
        # Manejar entrada del jugador (puede retornar una bala)
        bullet = self.player.handle_input(keys)
        
        # Si se disparó, agregar la bala
        if bullet:
            self.bullets.add(bullet)
            self.all_sprites.add(bullet)
            print(f"Disparo! Munición restante: {self.player.ammo}")
        
        # Actualizar balas
        for bullet in self.bullets:
            bullet.update()
        
        # ACTUALIZAR ENEMIGOS - Esto es lo que hace que se muevan
        for enemy in self.enemies:
            enemy.update(self.player)
            
            # Verificar colisión con jugador
            if enemy.alive and self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(enemy.damage)
                print(f"Jugador recibe daño! Vida: {self.player.health}")
        
        # Manejar colisiones balas-enemigos
        self.handle_bullet_collisions()
        
        # Verificar enemigos derrotados
        enemies_to_remove = []
        for enemy in self.enemies:
            if not enemy.alive:
                enemies_to_remove.append(enemy)
                self.enemies_defeated += 1
                print(f"Enemigo derrotado. Total: {self.enemies_defeated}/{self.total_enemies}")
        
        # Eliminar enemigos derrotados
        for enemy in enemies_to_remove:
            enemy.kill()
            self.enemies.remove(enemy)
        
        # Crear llave cuando todos los enemigos están muertos
        if self.enemies_defeated >= self.total_enemies and not self.key_found and not self.key:
            self.create_key()
            print("Llave creada!")
        
        # Recoger llave
        if self.key and not self.key_found:
            if self.player.rect.colliderect(self.key.rect):
                if keys[pygame.K_e]:
                    self.key_found = True
                    self.player_data["keys"] += 1
                    self.player.keys += 1
                    print(f"Llave recogida! Total llaves: {self.player.keys}")
                    self.key.kill()
        
        # Verificar si puede avanzar
        if self.key_found:
            if not self.exit_door:
                self.create_exit_door()
            
            if self.exit_door and self.player.rect.colliderect(self.exit_door):
                if keys[pygame.K_e]:
                    print("Siguiente nivel!")
                    return "next_level"
        
        # Verificar game over
        if self.player.health <= 0:
            print("Game Over!")
            return "game_over"
        
        # Actualizar datos del jugador
        self.player_data["health"] = self.player.health
        self.player_data["ammo"] = self.player.ammo
        self.player_data["keys"] = self.player.keys
        
        return None
        
    def create_key(self):
        """Crear la llave"""
        self.key = Key(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.all_sprites.add(self.key)
        
    def create_exit_door(self):
        """Crear la puerta de salida"""
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - 40, 50, 80)
        
    def draw(self):
        """Dibujar el nivel"""
        # Fondo
        self.screen.fill(BLACK)
        
        # Cuadrícula estilo museo
        for x in range(0, SCREEN_WIDTH, 50):
            for y in range(0, SCREEN_HEIGHT, 50):
                if (x + y) // 50 % 2 == 0:
                    pygame.draw.rect(self.screen, (25, 25, 25), (x, y, 50, 50), 1)
        
        # Dibujar sprites
        self.all_sprites.draw(self.screen)
        
        # Dibujar puerta de salida
        if self.exit_door:
            pygame.draw.rect(self.screen, (100, 100, 100), self.exit_door)
            pygame.draw.rect(self.screen, GREEN, self.exit_door.inflate(-10, -10))
            door_text = pygame.font.Font(None, 16).render("EXIT", True, BLACK)
            door_rect = door_text.get_rect(center=self.exit_door.center)
            self.screen.blit(door_text, door_rect)
            
            if self.player.rect.colliderect(self.exit_door):
                press_text = self.font.render("Presiona E para salir", True, YELLOW)
                press_rect = press_text.get_rect(center=(self.exit_door.centerx, self.exit_door.bottom + 15))
                self.screen.blit(press_text, press_rect)
        
        # UI
        self.draw_ui()
        
        # Título del nivel
        level_title = self.big_font.render(self.level_name, True, RED)
        title_rect = level_title.get_rect(center=(SCREEN_WIDTH // 2, 10))
        self.screen.blit(level_title, title_rect)
        
        # Contador de enemigos
        enemies_remaining = self.total_enemies - self.enemies_defeated
        enemy_text = self.font.render(f"ENEMIGOS: {enemies_remaining}", True, RED)
        self.screen.blit(enemy_text, (SCREEN_WIDTH // 2 - 60, 50))
        
        # Mensaje de tutorial
        if self.enemies_defeated == 0 and not self.key_found:
            tutorial = pygame.font.Font(None, 18).render(
                "¡DISPARA con ESPACIO! Elimina a los dinosaurios rojos", 
                True, YELLOW
            )
            tutorial_rect = tutorial.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(tutorial, tutorial_rect)

class Key(pygame.sprite.Sprite):
    """Llave para avanzar de nivel"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(YELLOW)
        pygame.draw.rect(self.image, ORANGE, (8, 2, 4, 16))
        pygame.draw.circle(self.image, ORANGE, (10, 2), 4)
        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.original_y = y
        self.animation_offset = 0
        
    def update(self):
        """Animación flotante"""
        self.animation_offset += 0.1
        self.rect.y = self.original_y + math.sin(self.animation_offset) * 5