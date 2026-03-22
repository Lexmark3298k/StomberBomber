"""
Clase Botón Temporal - Para activar/desactivar láseres
"""

import pygame
import math
from settings import *

class TemporalButton(pygame.sprite.Sprite):
    def __init__(self, x, y, activation_time=3):
        super().__init__()
        
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        self.activation_time = activation_time  # segundos
        self.is_pressed = False
        self.timer = 0
        self.cooldown = 0
        
        # Dibujar botón
        self.draw_button()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animación
        self.pulse_timer = 0
        
    def draw_button(self):
        """Dibujar el botón según su estado"""
        self.image.fill((0, 0, 0, 0))
        
        if self.is_pressed:
            color = GREEN
            # Efecto de presionado
            pygame.draw.rect(self.image, color, (10, 15, 30, 35))
            pygame.draw.circle(self.image, (0, 255, 0, 100), (25, 25), 15)
        else:
            color = BUTTON_COLOR
            pygame.draw.rect(self.image, color, (8, 13, 34, 39))
            pygame.draw.circle(self.image, (100, 100, 255, 100), (25, 25), 12)
            
        # Marco
        pygame.draw.rect(self.image, WHITE, (5, 10, 40, 45), 2)
        
        # Texto
        font = pygame.font.Font(None, 20)
        text = font.render("B", True, WHITE)
        self.image.blit(text, (21, 25))
        
    def update(self):
        """Actualizar temporizador del botón"""
        current_time = pygame.time.get_ticks()
        
        if self.is_pressed:
            if current_time - self.timer > self.activation_time * 1000:
                self.is_pressed = False
                self.draw_button()
                
        # Animación de pulso cuando no está presionado
        if not self.is_pressed:
            self.pulse_timer += 0.1
            pulse = abs(math.sin(self.pulse_timer)) * 50
            self.image.set_alpha(200 + pulse)
                
    def interact(self):
        """Interactuar con el botón"""
        current_time = pygame.time.get_ticks()
        
        if not self.is_pressed and current_time > self.cooldown:
            self.is_pressed = True
            self.timer = current_time
            self.draw_button()
            return True
        return False
        
    def get_state(self):
        """Devolver estado actual (True = láseres desactivados)"""
        return self.is_pressed