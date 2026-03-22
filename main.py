"""
Stomber Bomber - Versión de prueba
"""

import pygame
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from settings import init_pygame, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BLACK, WHITE, RED, GREEN, YELLOW, CYAN
from game_state import GameState

class StomberBomber:
    def __init__(self):
        self.screen = init_pygame()
        self.clock = pygame.time.Clock()
        self.game_state = GameState(self.screen)
        self.running = True
        self.font = pygame.font.Font(None, 36)
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.game_state.update()
            self.game_state.draw()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    print("=== STOMBER BOMBER ===")
    print("Controles: WASD mover, ESPACIO disparar, E interactuar")
    print("Elimina a los 3 dinosaurios rojos para obtener la llave")
    game = StomberBomber()
    game.run()