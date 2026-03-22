"""
Salón 3 - Muro de la Muerte
Mecánica: Laberinto de láseres con botón temporal
"""

import pygame
import math
from levels.level_base import LevelBase
from classes.player import Player
from classes.laser import Laser
from classes.button import TemporalButton
from settings import *

class Salon3(LevelBase):
    def __init__(self, screen, player_data):
        super().__init__(screen, player_data)
        
        self.level_name = "MURO DE LA MUERTE"
        
        # Crear jugador
        self.player = Player(50, 300, player_data)
        self.all_sprites.add(self.player)
        
        # Zona segura inicial
        self.safe_zone = pygame.Rect(30, 250, 100, 100)
        self.player.in_safe_zone = True
        
        # Crear laberinto de láseres
        self.lasers = pygame.sprite.Group()
        self.create_laser_maze()
        
        # Crear botón central
        self.button = TemporalButton(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT // 2 - 25, activation_time=3)
        self.all_sprites.add(self.button)
        self.buttons = pygame.sprite.Group()
        self.buttons.add(self.button)
        
        # Variables del nivel
        self.key_found = False
        self.key_position = (750, 300)
        self.key = None
        self.exit_door = None
        self.lasers_active = True
        
        # Temporizador para UI
        self.timer_display = 0
        
        print(f"Salón 3 iniciado. Láseres activos: {self.lasers_active}")
        
    def create_laser_maze(self):
        """Crear un patrón de láseres estilo laberinto"""
        
        # Láseres horizontales
        lasers_config = [
            (100, 120, 700, 120),   # Superior
            (100, 220, 700, 220),   # Medio superior
            (100, 380, 700, 380),   # Medio inferior
            (100, 480, 700, 480),   # Inferior
            
            # Láseres verticales (intercalados)
            (200, 150, 200, 250),
            (350, 80, 350, 200),
            (350, 300, 350, 450),
            (500, 200, 500, 350),
            (500, 400, 500, 520),
            (650, 250, 650, 450),
        ]
        
        for x1, y1, x2, y2 in lasers_config:
            laser = Laser(x1, y1, x2, y2)
            self.lasers.add(laser)
            self.all_sprites.add(laser)
            
        # Añadir algunos láseres diagonales para más desafío
        diag_lasers = [
            (250, 100, 350, 200),
            (450, 500, 550, 400),
            (600, 100, 700, 200),
        ]
        
        for x1, y1, x2, y2 in diag_lasers:
            laser = Laser(x1, y1, x2, y2, "diagonal")
            self.lasers.add(laser)
            self.all_sprites.add(laser)
            
    def update(self):
        """Actualizar lógica del nivel"""
        keys = pygame.key.get_pressed()
        
        # Manejar entrada del jugador (sin disparos en este nivel)
        self.player.handle_input(keys)
        
        # Verificar zona segura
        self.player.in_safe_zone = self.safe_zone.colliderect(self.player.rect)
        
        # Interacción con botón
        if keys[pygame.K_e]:
            if self.player.rect.colliderect(self.button.rect):
                if self.button.interact():
                    print("¡Botón activado! Láseres desactivados por 3 segundos")
                    
        # Actualizar botón
        self.button.update()
        
        # Estado de láseres: activos si el botón NO está presionado
        self.lasers_active = not self.button.get_state()
        
        # Actualizar láseres
        for laser in self.lasers:
            laser.update(self.lasers_active)
            
        # Verificar colisiones con láseres
        if self.lasers_active:
            for laser in self.lasers:
                if laser.check_collision(self.player.rect):
                    self.player.take_damage(laser.damage)
                    print("¡Jugador tocó un láser!")
                    # Empujar al jugador hacia atrás
                    self.player.knockback(laser.rect.center)
                    
        # Mostrar llave solo cuando láseres desactivados
        if not self.lasers_active and not self.key_found:
            self.show_key()
            
        # Recoger llave
        if self.key and not self.key_found:
            if self.player.rect.colliderect(self.key.rect):
                if keys[pygame.K_e]:
                    self.key_found = True
                    self.player_data["keys"] += 1
                    self.player.keys += 1
                    print(f"¡Llave encontrada! Llaves: {self.player.keys}")
                    self.key.kill()
                    
        # Crear puerta de salida
        if self.key_found and not self.exit_door:
            self.create_exit_door()
            
        # Verificar salida
        if self.exit_door and self.player.rect.colliderect(self.exit_door):
            if keys[pygame.K_e]:
                print("¡Salón 3 completado!")
                return "next_level"
                
        # Verificar game over
        if self.player.health <= 0:
            print("Game Over en Salón 3!")
            return "game_over"
            
        # Actualizar datos
        self.player_data["health"] = self.player.health
        self.player_data["keys"] = self.player.keys
        
        return None
        
    def show_key(self):
        """Mostrar llave cuando láseres desactivados"""
        if not self.key:
            self.key = Key(self.key_position[0], self.key_position[1])
            self.all_sprites.add(self.key)
            
    def create_exit_door(self):
        """Crear puerta de salida"""
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - 40, 50, 80)
        
    def draw(self):
        """Dibujar el nivel"""
        self.screen.fill(BLACK)
        
        # Dibujar piso estilo tecnológico
        for x in range(0, SCREEN_WIDTH, 40):
            for y in range(0, SCREEN_HEIGHT, 40):
                color = (20, 20, 30) if (x + y) // 40 % 2 == 0 else (30, 30, 40)
                pygame.draw.rect(self.screen, color, (x, y, 40, 40))
                
        # Dibujar sprites
        self.all_sprites.draw(self.screen)
        
        # Dibujar zona segura
        safe_surf = pygame.Surface((100, 100))
        safe_surf.set_alpha(80)
        safe_surf.fill(DARK_GREEN)
        self.screen.blit(safe_surf, (30, 250))
        pygame.draw.rect(self.screen, GREEN, self.safe_zone, 2)
        
        safe_text = pygame.font.Font(None, 14).render("ZONA SEGURA", True, GREEN)
        self.screen.blit(safe_text, (35, 260))
        
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
        
        # Título
        title = self.big_font.render(self.level_name, True, LASER_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 10))
        self.screen.blit(title, title_rect)
        
        # Indicador de estado de láseres
        if self.lasers_active:
            laser_text = self.font.render("⚠️ LÁSERES ACTIVOS ⚠️", True, RED)
            laser_rect = laser_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            self.screen.blit(laser_text, laser_rect)
        else:
            # Temporizador
            remaining = 3 - (pygame.time.get_ticks() - self.button.timer) / 1000 if self.button.is_pressed else 0
            if remaining > 0:
                timer_text = self.font.render(f"🔓 LÁSERES DESACTIVADOS: {remaining:.1f}s 🔓", True, GREEN)
                timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
                self.screen.blit(timer_text, timer_rect)
                
        # Mensaje de tutorial
        if not self.key_found and self.lasers_active:
            tutorial = pygame.font.Font(None, 16).render(
                "Corre hacia el BOTÓN (cuadro azul) y presiona E para desactivar los láseres", 
                True, YELLOW
            )
            tutorial_rect = tutorial.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(tutorial, tutorial_rect)
        elif not self.key_found and not self.lasers_active:
            tutorial = pygame.font.Font(None, 16).render(
                "¡RÁPIDO! Corre hacia la LLAVE mientras los láseres están desactivados", 
                True, CYAN
            )
            tutorial_rect = tutorial.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(tutorial, tutorial_rect)

class Key(pygame.sprite.Sprite):
    """Llave para avanzar"""
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
        self.animation_offset += 0.1
        self.rect.y = self.original_y + math.sin(self.animation_offset) * 5