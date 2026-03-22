os.chdir(os.path.dirname(os.path.abspath(__file__)))
"""
Stomber Bomber - Main Game Loop
Estilo DOS / Retro


"""

import pygame
import sys
import os

from settings import init_pygame, SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from game_state import GameState

class StomberBomber:
    def __init__(self):
        """Inicializa el juego"""
        self.screen = init_pygame()
        self.clock = pygame.time.Clock()
        self.game_state = GameState(self.screen)
        self.running = True
        
        # Fuente retro para UI
        try:
            self.font = pygame.font.Font("assets/fonts/press_start.ttf", 24)
        except:
            self.font = pygame.font.Font(None, 24)
            
        # Pantalla de título
        self.show_title_screen()
        
    def show_title_screen(self):
        """Muestra la pantalla de título estilo DOS"""
        title_running = True
        
        # Crear efecto de parpadeo para "Press any key"
        blink_timer = 0
        show_text = True
        
        while title_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    title_running = False  # Cualquier tecla inicia el juego
                    
            # Dibujar pantalla de título
            self.screen.fill(BLACK)
            
            # Título principal
            title_text = self.font.render("STOMBER BOMBER", True, RED)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(title_text, title_rect)
            
            # Subtítulo
            subtitle = self.font.render("Jurassic Mayhem", True, YELLOW)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 220))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Dibujar un dinosaurio ASCII art simple
            dino_art = [
                "    __",
                "  <(o )___",
                "   ( ._> /",
                "    `---'"
            ]
            y_offset = 280
            for line in dino_art:
                dino_text = pygame.font.Font(None, 20).render(line, True, GREEN)
                dino_rect = dino_text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                self.screen.blit(dino_text, dino_rect)
                y_offset += 20
                
            # Texto de Dr. Denied
            denied_text = pygame.font.Font(None, 18).render("Dr. Denied te ha atrapado en su museo...", True, WHITE)
            denied_rect = denied_text.get_rect(center=(SCREEN_WIDTH//2, 400))
            self.screen.blit(denied_text, denied_rect)
            
            # Efecto de parpadeo para "Press any key"
            blink_timer += 1
            if blink_timer > 30:
                blink_timer = 0
                show_text = not show_text
                
            if show_text:
                press_text = self.font.render("PRESS ANY KEY", True, CYAN)
                press_rect = press_text.get_rect(center=(SCREEN_WIDTH//2, 500))
                self.screen.blit(press_text, press_rect)
                
            pygame.display.flip()
            self.clock.tick(30)
            
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        
            # Actualizar estado del juego
            result = self.game_state.update()
            
            # Verificar cambios de estado
            if result == "quit":
                self.running = False
            elif result == "game_over":
                self.show_game_over()
            elif result == "victory":
                self.show_victory()
                
            # Dibujar
            self.game_state.draw()
            
            # Actualizar pantalla
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()
        
    def show_game_over(self):
        """Pantalla de Game Over"""
        self.screen.fill(BLACK)
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = pygame.font.Font(None, 24).render("Press R to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.game_state = GameState(self.screen)
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
    def show_victory(self):
        """Pantalla de Victoria"""
        self.screen.fill(BLACK)
        
        victory_text = self.font.render("VICTORY!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        credits_text = pygame.font.Font(None, 24).render("Has derrotado a Dante y escapado del museo!", True, YELLOW)
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(credits_text, credits_rect)
        
        thanks_text = pygame.font.Font(None, 20).render("Gracias por jugar - Press ESC to exit", True, WHITE)
        thanks_rect = thanks_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(thanks_text, thanks_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    waiting = False
                    
if __name__ == "__main__":
    game = StomberBomber()
    game.run()