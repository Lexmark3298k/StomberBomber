"""
Game State Manager - Maneja la transición entre niveles
"""

import pygame
from levels.salon1 import Salon1
from levels.salon2 import Salon2
from levels.salon3 import Salon3  # Agregar al inicio
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, WHITE, YELLOW

class GameState:
    def __init__(self, screen):
        self.screen = screen
        self.current_level = 1
        self.max_level = 5
        self.level = None
        self.transition_timer = 0
        self.transition_active = False
        self.next_level = None
        self.player_data = {
            "health": 100,
            "keys": 0,
            "ammo": 30
        }
        
        # Cargar primer nivel
        self.load_level()
        
        # Fuente para transiciones
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 24)
        
    def load_level(self):
        """Carga el nivel actual - VERSION CORREGIDA"""
        if self.current_level == 1:
            self.level = Salon1(self.screen, self.player_data)
            print("Cargando Salón 1: Combate")
        elif self.current_level == 2:
            self.level = Salon2(self.screen, self.player_data)
            print("Cargando Salón 2: Sigilo")
        elif self.current_level == 3:
            self.level = Salon3(self.screen, self.player_data)
            print("Cargando Salón 3: Láseres")
        elif self.current_level == 4:
            # self.level = Salon4(self.screen, self.player_data)
            print("Salón 4: Próximamente")
            return "victory"
        elif self.current_level == 5:
            # self.level = Salon5(self.screen, self.player_data)
            print("Salón 5: Próximamente")
            return "victory"
        else:
            # Más allá del nivel 5, victoria final
            return "victory"
            
        return None
        
    def update(self):
        """Actualiza el estado actual"""
        if self.transition_active:
            self.transition_timer -= 1
            if self.transition_timer <= 0:
                self.transition_active = False
                self.current_level = self.next_level
                result = self.load_level()
                if result == "victory":
                    return "victory"
            return None
            
        # Actualizar nivel actual
        if self.level:
            result = self.level.update()
            
            if result == "next_level":
                self.start_transition(self.current_level + 1)
            elif result == "game_over":
                return "game_over"
            elif result == "quit":
                return "quit"
                
        return None
        
    def start_transition(self, next_level):
        """Inicia la transición entre niveles"""
        self.transition_active = True
        self.transition_timer = 60
        self.next_level = next_level
        
    def draw(self):
        """Dibuja el estado actual"""
        if self.transition_active:
            if self.level:
                self.level.draw()
            
            # Overlay de transición
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Texto de transición
            if self.next_level <= self.max_level:
                text = self.font.render(f"SALON {self.next_level}", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
                self.screen.blit(text, text_rect)
                
                # Nombres de los salones
                level_names = {
                    1: "CARNICERIA CRETACICA",
                    2: "SALA DE LOS ECOS",
                    3: "MURO DE LA MUERTE",
                    4: "ESTATICA MORTAL",
                    5: "DANZA CON DANTE"
                }
                
                sub_text = self.small_font.render(
                    level_names.get(self.next_level, ""), 
                    True, YELLOW
                )
                sub_rect = sub_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
                self.screen.blit(sub_text, sub_rect)
                
                # Animación de carga
                dots = "." * ((pygame.time.get_ticks() // 300) % 4)
                loading_text = self.small_font.render(f"Cargando{dots}", True, WHITE)
                loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 70))
                self.screen.blit(loading_text, loading_rect)
        else:
            if self.level:
                self.level.draw()