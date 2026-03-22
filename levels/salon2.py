"""
Salón 2 - Sala de los Ecos
Mecánica: Sigilo - Evadir a los Raptores Fantasma
"""

import pygame
import math
from levels.level_base import LevelBase
from classes.player import Player
from classes.enemies import RaptorFantasma
from classes.hiding_spot import HidingSpot
from settings import *

class Salon2(LevelBase):
    def __init__(self, screen, player_data):
        super().__init__(screen, player_data)
        
        self.level_name = "SALA DE LOS ECOS"
        
        # Crear jugador
        self.player = Player(100, 300, player_data)
        self.player.in_safe_zone = True
        self.all_sprites.add(self.player)
        
        # Lista de obstáculos para línea de visión
        self.obstacles = []
        
        # Crear escondites
        self.hiding_spots = pygame.sprite.Group()
        spots_positions = [
            (150, 150, "fossil"),
            (350, 450, "exhibit"),
            (600, 200, "bush"),
            (450, 100, "fossil"),
            (700, 500, "exhibit")
        ]
        
        for x, y, spot_type in spots_positions:
            spot = HidingSpot(x, y, spot_type)
            self.hiding_spots.add(spot)
            self.all_sprites.add(spot)
            
        # Crear Raptores Fantasma con rutas de patrulla
        self.enemies = pygame.sprite.Group()
        
        # Raptor 1 - Patrulla horizontal
        patrol_1 = [(200, 200), (400, 200), (400, 300), (200, 300)]
        raptor1 = RaptorFantasma(200, 200, patrol_1)
        self.enemies.add(raptor1)
        self.all_sprites.add(raptor1)
        
        # Raptor 2 - Patrulla vertical
        patrol_2 = [(600, 400), (600, 200), (500, 200), (500, 400)]
        raptor2 = RaptorFantasma(600, 300, patrol_2)
        self.enemies.add(raptor2)
        self.all_sprites.add(raptor2)
        
        # Raptor 3 - Patrulla circular
        patrol_3 = [(300, 500), (400, 500), (400, 400), (300, 400)]
        raptor3 = RaptorFantasma(350, 450, patrol_3)
        self.enemies.add(raptor3)
        self.all_sprites.add(raptor3)
        
        # Variables de nivel
        self.total_enemies = len(self.enemies)
        self.key_found = False
        self.key = None
        self.key_position = (750, 550)  # Llave escondida al fondo
        self.exit_door = None
        
        # Barra de alerta global
        self.global_alert = 0
        self.alert_bar_surface = pygame.Surface((300, 25))
        
        # Sistema de detección
        self.detection_timer = 0
        self.detection_pulse = 0
        
        # Zona segura de inicio
        self.safe_zone = pygame.Rect(50, 250, 150, 150)
        
        # Llave interactuable
        self.key_visible = False
        self.key_interact_rect = pygame.Rect(self.key_position[0] - 15, self.key_position[1] - 15, 30, 30)
        
        print(f"Salón 2 iniciado. Raptores: {self.total_enemies}")
        
    def update(self):
        """Actualizar lógica del nivel de sigilo"""
        keys = pygame.key.get_pressed()
        
        # Manejar entrada del jugador
        self.player.handle_input(keys)
        
        # Verificar zona segura
        self.player.in_safe_zone = self.safe_zone.colliderect(self.player.rect)
        if self.player.in_safe_zone:
            # Regenerar vida lentamente en zona segura
            if self.player.health < self.player.max_health:
                self.player.health = min(self.player.max_health, self.player.health + 0.2)
                self.player_data["health"] = self.player.health
                
        # Verificar interacción con escondites
        if keys[pygame.K_e]:
            for spot in self.hiding_spots:
                if self.player.rect.colliderect(spot.rect):
                    if spot.interact(self.player):
                        print("Jugador escondido!")
                        break
                        
        # Salir del escondite (presionar E de nuevo o moverse)
        if self.player.is_hiding:
            if keys[pygame.K_e] or any([keys[pygame.K_w], keys[pygame.K_a], keys[pygame.K_s], keys[pygame.K_d]]):
                self.player.unhide()
                if self.player.current_hiding_spot:
                    self.player.current_hiding_spot.get_out()
                    self.player.current_hiding_spot = None
                    
        # Actualizar escondites con distancia al jugador
        for spot in self.hiding_spots:
            dx = self.player.rect.centerx - spot.rect.centerx
            dy = self.player.rect.centery - spot.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            spot.update(distance)
            
        # Actualizar enemigos con obstáculos
        for enemy in self.enemies:
            enemy.update(self.player, self.obstacles)
            
            # Verificar colisión con jugador (ataque)
            if not self.player.is_hiding and self.player.rect.colliderect(enemy.rect):
                self.player.take_damage(15)
                print(f"¡Atrapado! Vida: {self.player.health}")
                
        # Calcular nivel de alerta global
        self.global_alert = max([e.alert_level for e in self.enemies]) if self.enemies else 0
        
        # Efecto de pulso cuando hay alerta alta
        if self.global_alert > 50:
            self.detection_pulse = (self.detection_pulse + 0.1) % (math.pi * 2)
            
        # Mostrar llave solo cuando el jugador está cerca y no está siendo perseguido
        player_near_key = math.sqrt(
            (self.player.rect.centerx - self.key_position[0])**2 +
            (self.player.rect.centery - self.key_position[1])**2
        ) < 50
        
        self.key_visible = player_near_key and self.global_alert < 30
        
        # Recoger llave
        if not self.key_found and self.key_visible:
            if keys[pygame.K_e]:
                self.key_found = True
                self.player_data["keys"] += 1
                self.player.keys += 1
                print(f"¡Llave encontrada! Llaves totales: {self.player.keys}")
                
        # Crear puerta de salida
        if self.key_found and not self.exit_door:
            self.create_exit_door()
            
        # Verificar salida
        if self.exit_door and self.player.rect.colliderect(self.exit_door):
            if keys[pygame.K_e]:
                print("¡Nivel completado!")
                return "next_level"
                
        # Verificar game over
        if self.player.health <= 0:
            print("Game Over!")
            return "game_over"
            
        # Actualizar datos del jugador
        self.player_data["health"] = self.player.health
        self.player_data["keys"] = self.player.keys
        
        return None
        
    def create_exit_door(self):
        """Crear la puerta de salida"""
        self.exit_door = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT // 2 - 40, 50, 80)
        
    def draw(self):
        """Dibujar el nivel de sigilo"""
        self.screen.fill(BLACK)
        
        # Dibujar piso estilo museo
        for x in range(0, SCREEN_WIDTH, 50):
            for y in range(0, SCREEN_HEIGHT, 50):
                if (x + y) // 50 % 2 == 0:
                    pygame.draw.rect(self.screen, (25, 25, 35), (x, y, 50, 50), 1)
                else:
                    pygame.draw.rect(self.screen, (35, 35, 45), (x, y, 50, 50), 1)
                    
        # Dibujar zona segura
        safe_zone_surf = pygame.Surface((150, 150))
        safe_zone_surf.set_alpha(50)
        safe_zone_surf.fill(DARK_GREEN)
        self.screen.blit(safe_zone_surf, (50, 250))
        pygame.draw.rect(self.screen, GREEN, self.safe_zone, 2)
        
        safe_text = pygame.font.Font(None, 16).render("ZONA SEGURA", True, GREEN)
        self.screen.blit(safe_text, (70, 270))
        
        # Dibujar escondites y sprites
        self.all_sprites.draw(self.screen)
        
        # Dibujar conos de visión de los enemigos (opcional - solo para debug)
        if self.global_alert > 20:  # Mostrar solo cuando hay alerta
            for enemy in self.enemies:
                if enemy.alert_level > 20:
                    self.draw_vision_cone(enemy)
                    
        # Dibujar llave
        if self.key_visible and not self.key_found:
            # Dibujar llave brillante
            glow = 100 + math.sin(pygame.time.get_ticks() * 0.005) * 50
            key_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(key_surf, (YELLOW[0], YELLOW[1], YELLOW[2], glow), (20, 20), 15)
            self.screen.blit(key_surf, (self.key_position[0] - 20, self.key_position[1] - 20))
            
            # Dibujar llave
            pygame.draw.rect(self.screen, YELLOW, (self.key_position[0] - 5, self.key_position[1] - 2, 10, 25))
            pygame.draw.circle(self.screen, YELLOW, (self.key_position[0], self.key_position[1] - 5), 8)
            
            # Texto interactivo
            if self.player.rect.colliderect(self.key_interact_rect):
                key_text = self.font.render("Presiona E para recoger la llave", True, YELLOW)
                key_rect = key_text.get_rect(center=(self.key_position[0], self.key_position[1] - 30))
                self.screen.blit(key_text, key_rect)
                
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
                
        # Dibujar barra de alerta
        self.draw_alert_bar()
        
        # Dibujar UI
        self.draw_ui()
        
        # Título del nivel
        level_title = self.big_font.render(self.level_name, True, (150, 150, 255))
        title_rect = level_title.get_rect(center=(SCREEN_WIDTH // 2, 10))
        self.screen.blit(level_title, title_rect)
        
        # Mensaje de estado
        if self.player.is_hiding:
            hide_text = self.font.render("¡ESCONDIDO! Los enemigos no te ven", True, CYAN)
            hide_rect = hide_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(hide_text, hide_rect)
        elif self.global_alert > 70:
            danger_text = self.font.render("¡TE HAN VISTO! ¡CORRE!", True, RED)
            danger_rect = danger_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            self.screen.blit(danger_text, danger_rect)
            
        # Tutorial si es necesario
        if not self.key_found and self.global_alert < 20:
            tutorial = pygame.font.Font(None, 18).render(
                "EVITA a los raptores azules | ESCÓNDETE en los objetos marrones (E) | Encuentra la llave", 
                True, YELLOW
            )
            tutorial_rect = tutorial.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
            self.screen.blit(tutorial, tutorial_rect)
            
    def draw_vision_cone(self, enemy):
        """Dibujar cono de visión del enemigo (debug/estilo)"""
        if not hasattr(enemy, 'facing_angle'):
            return
            
        # Calcular puntos del cono
        angle_rad = math.radians(enemy.facing_angle)
        left_angle = angle_rad - math.radians(enemy.vision_angle / 2)
        right_angle = angle_rad + math.radians(enemy.vision_angle / 2)
        
        points = [enemy.rect.center]
        for angle in [left_angle, right_angle]:
            x = enemy.rect.centerx + math.cos(angle) * enemy.vision_range
            y = enemy.rect.centery + math.sin(angle) * enemy.vision_range
            points.append((x, y))
            
        # Dibujar cono semitransparente
        if len(points) >= 3:
            cone_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = min(80, enemy.alert_level)
            pygame.draw.polygon(cone_surf, (255, 100, 100, alpha), points)
            self.screen.blit(cone_surf, (0, 0))
            
    def draw_alert_bar(self):
        """Dibujar barra de alerta global"""
        alert_percentage = self.global_alert / 100
        
        # Fondo
        pygame.draw.rect(self.screen, (64, 0, 0), (SCREEN_WIDTH // 2 - 150, 50, 300, 20))
        
        # Color según nivel de alerta
        if alert_percentage > 0.7:
            alert_color = RED
        elif alert_percentage > 0.3:
            alert_color = YELLOW
        else:
            alert_color = GREEN
            
        # Barra con efecto de pulso
        if self.global_alert > 50:
            pulse = math.sin(self.detection_pulse) * 10
            width = 300 * alert_percentage + pulse
        else:
            width = 300 * alert_percentage
            
        pygame.draw.rect(self.screen, alert_color, (SCREEN_WIDTH // 2 - 150, 50, width, 20))
        
        # Texto
        alert_text = self.font.render(f"ALERTA: {int(self.global_alert)}%", True, WHITE)
        alert_rect = alert_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
        self.screen.blit(alert_text, alert_rect)