"""
Stomber Bomber - Main Game Loop (Versión de prueba - CORREGIDA)
"""

import pygame
import sys
import os

# Cambiar al directorio del script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Importar configuración con todos los colores necesarios
try:
    from settings import (
        init_pygame, SCREEN_WIDTH, SCREEN_HEIGHT, FPS,
        BLACK, RED, GREEN, YELLOW, CYAN, WHITE, BLUE, GRAY
    )
except ImportError as e:
    print(f"Error importando settings: {e}")
    # Si falla la importación, definir colores básicos aquí mismo
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    GRAY = (128, 128, 128)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60
    
    def init_pygame():
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("STOMBER BOMBER - Jurassic Mayhem")
        return screen

class StomberBomber:
    def __init__(self):
        """Inicializa el juego"""
        try:
            self.screen = init_pygame()
        except Exception as e:
            print(f"Error inicializando pygame: {e}")
            sys.exit(1)
            
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Fuente simple si no hay la retro
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Variables de juego simplificadas para prueba
        self.game_started = False
        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
        self.player_health = 100
        self.player_keys = 0
        
        # Para animación del título
        self.title_animation = 0
        self.title_direction = 1
        
    def run(self):
        """Bucle principal del juego"""
        while self.running:
            dt = self.clock.tick(FPS)
            
            # Manejar eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE and not self.game_started:
                        self.game_started = True
                    # Reiniciar juego con R
                    if event.key == pygame.K_r and self.game_started:
                        self.player_health = 100
                        self.player_keys = 0
                        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
                        
            # Actualizar
            if self.game_started:
                self.update()
            else:
                # Animación del título
                self.title_animation += self.title_direction * 2
                if self.title_animation > 10 or self.title_animation < -10:
                    self.title_direction *= -1
                    
            # Dibujar
            self.draw()
            
            pygame.display.flip()
            
        pygame.quit()
        sys.exit()
        
    def update(self):
        """Actualizar lógica del juego"""
        keys = pygame.key.get_pressed()
        
        # Movimiento del jugador
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player_pos[0] -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player_pos[0] += 5
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.player_pos[1] -= 5
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.player_pos[1] += 5
            
        # Limitar a la pantalla
        self.player_pos[0] = max(0, min(self.player_pos[0], SCREEN_WIDTH - 40))
        self.player_pos[1] = max(0, min(self.player_pos[1], SCREEN_HEIGHT - 40))
        
        # Probar tecla E para recoger llaves (demo)
        if keys[pygame.K_e]:
            # Simular recoger llave cuando pasa sobre una zona
            if self.player_pos[0] > SCREEN_WIDTH - 100 and self.player_pos[1] > SCREEN_HEIGHT - 100:
                if self.player_keys < 3:
                    self.player_keys += 1
                    # Pequeño retraso para no recoger múltiples
                    pygame.time.wait(200)
        
    def draw(self):
        """Dibujar el juego"""
        self.screen.fill(BLACK)
        
        if not self.game_started:
            # Pantalla de título con animación
            
            # Efecto de "scanlines" (líneas de escaneo estilo DOS)
            for y in range(0, SCREEN_HEIGHT, 4):
                pygame.draw.line(self.screen, (10, 10, 10), (0, y), (SCREEN_WIDTH, y), 1)
            
            # Título con efecto de temblor
            title_y = 150 + self.title_animation
            title = self.font.render("STOMBER BOMBER", True, RED)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, title_y))
            self.screen.blit(title, title_rect)
            
            # Sombra del título
            title_shadow = self.font.render("STOMBER BOMBER", True, (100, 0, 0))
            shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + 3, title_y + 3))
            self.screen.blit(title_shadow, shadow_rect)
            
            # Subtítulo
            subtitle = self.small_font.render("Jurassic Mayhem", True, YELLOW)
            subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH//2, 210))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Marco decorativo estilo DOS
            pygame.draw.rect(self.screen, CYAN, (50, 250, SCREEN_WIDTH - 100, 150), 2)
            
            # Texto de historia
            story_lines = [
                "Dr. Denied ha revivido dinosaurios",
                "cyberneticamente modificados",
                "y te ha encerrado en su MUSEO."
            ]
            y_offset = 280
            for line in story_lines:
                story_text = pygame.font.Font(None, 20).render(line, True, WHITE)
                story_rect = story_text.get_rect(center=(SCREEN_WIDTH//2, y_offset))
                self.screen.blit(story_text, story_rect)
                y_offset += 25
                
            # Texto de "Press Space" con efecto de parpadeo
            blink = (pygame.time.get_ticks() // 500) % 2
            if blink:
                press_text = self.font.render("PRESS SPACE", True, CYAN)
                press_rect = press_text.get_rect(center=(SCREEN_WIDTH//2, 450))
                self.screen.blit(press_text, press_rect)
            
            # Créditos
            credits = pygame.font.Font(None, 14).render("STOMBER BOMBER vs DR. DENIED", True, GRAY)
            credits_rect = credits.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
            self.screen.blit(credits, credits_rect)
            
        else:
            # ========== JUEGO ==========
            
            # Dibujar un piso simple estilo cuadrícula
            for x in range(0, SCREEN_WIDTH, 50):
                for y in range(0, SCREEN_HEIGHT, 50):
                    if (x + y) % 100 == 0:
                        pygame.draw.rect(self.screen, (20, 20, 20), (x, y, 50, 50), 1)
            
            # Dibujar al jugador (cuadro azul con cara)
            pygame.draw.rect(self.screen, BLUE, (self.player_pos[0], self.player_pos[1], 40, 40))
            # Ojos del personaje
            if self.player_health > 50:
                eye_color = WHITE
            else:
                eye_color = YELLOW
            pygame.draw.circle(self.screen, eye_color, (self.player_pos[0] + 10, self.player_pos[1] + 15), 5)
            pygame.draw.circle(self.screen, eye_color, (self.player_pos[0] + 30, self.player_pos[1] + 15), 5)
            pygame.draw.circle(self.screen, BLACK, (self.player_pos[0] + 10, self.player_pos[1] + 15), 2)
            pygame.draw.circle(self.screen, BLACK, (self.player_pos[0] + 30, self.player_pos[1] + 15), 2)
            
            # Zona de llave de prueba (esquina inferior derecha)
            key_zone = pygame.Rect(SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80, 60, 60)
            pygame.draw.rect(self.screen, YELLOW, key_zone, 2)
            if self.player_keys < 3:
                pygame.draw.polygon(self.screen, YELLOW, [
                    (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50),
                    (SCREEN_WIDTH - 55, SCREEN_HEIGHT - 40),
                    (SCREEN_WIDTH - 45, SCREEN_HEIGHT - 40)
                ])
                key_text = self.small_font.render("E", True, YELLOW)
                self.screen.blit(key_text, (SCREEN_WIDTH - 65, SCREEN_HEIGHT - 65))
            
            # Dibujar un enemigo de prueba (cuadrado rojo)
            enemy_pos = (400, 300)
            pygame.draw.rect(self.screen, RED, (enemy_pos[0], enemy_pos[1], 40, 40))
            # Ojos malvados
            pygame.draw.circle(self.screen, WHITE, (enemy_pos[0] + 10, enemy_pos[1] + 15), 4)
            pygame.draw.circle(self.screen, WHITE, (enemy_pos[0] + 30, enemy_pos[1] + 15), 4)
            pygame.draw.circle(self.screen, RED, (enemy_pos[0] + 10, enemy_pos[1] + 15), 2)
            pygame.draw.circle(self.screen, RED, (enemy_pos[0] + 30, enemy_pos[1] + 15), 2)
            
            # Colisión simple con enemigo (si toca, pierde vida)
            player_rect = pygame.Rect(self.player_pos[0], self.player_pos[1], 40, 40)
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], 40, 40)
            if player_rect.colliderect(enemy_rect):
                self.player_health -= 1
                # Empujar al jugador hacia atrás
                if self.player_pos[0] < enemy_pos[0]:
                    self.player_pos[0] -= 20
                else:
                    self.player_pos[0] += 20
                if self.player_pos[1] < enemy_pos[1]:
                    self.player_pos[1] -= 20
                else:
                    self.player_pos[1] += 20
                    
            # ========== UI ==========
            
            # Barra de vida con gradiente
            health_percentage = max(0, self.player_health / 100)
            pygame.draw.rect(self.screen, (64, 0, 0), (20, 20, 200, 25))
            
            # Cambiar color según la vida
            if health_percentage > 0.6:
                health_color = GREEN
            elif health_percentage > 0.3:
                health_color = YELLOW
            else:
                health_color = RED
                
            pygame.draw.rect(self.screen, health_color, (20, 20, 200 * health_percentage, 25))
            
            # Texto de vida
            health_text = self.small_font.render(f"HP: {self.player_health}", True, WHITE)
            self.screen.blit(health_text, (20, 48))
            
            # Llaves
            keys_text = self.small_font.render(f"KEYS: {self.player_keys}/3", True, YELLOW)
            self.screen.blit(keys_text, (SCREEN_WIDTH - 100, 20))
            
            # Dibujar llaves obtenidas
            for i in range(self.player_keys):
                pygame.draw.polygon(self.screen, YELLOW, [
                    (SCREEN_WIDTH - 120 + (i * 25), 45),
                    (SCREEN_WIDTH - 125 + (i * 25), 55),
                    (SCREEN_WIDTH - 115 + (i * 25), 55)
                ])
            
            # Mensaje si completó las llaves
            if self.player_keys >= 3:
                complete_text = self.font.render("¡PUERTA ABIERTA! Ve a la salida", True, GREEN)
                complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(complete_text, complete_rect)
                
                # Puerta de salida
                exit_door = pygame.Rect(SCREEN_WIDTH - 100, SCREEN_HEIGHT//2 - 50, 60, 100)
                pygame.draw.rect(self.screen, GREEN, exit_door)
                door_text = self.small_font.render("EXIT", True, BLACK)
                self.screen.blit(door_text, (SCREEN_WIDTH - 85, SCREEN_HEIGHT//2 - 10))
                
                # Verificar si toca la puerta
                if player_rect.colliderect(exit_door):
                    # Victoria
                    self.show_victory()
            
            # Verificar game over
            if self.player_health <= 0:
                self.show_game_over()
            
            # Instrucciones
            controls = self.small_font.render("WASD: Mover | E: Recoger | R: Reiniciar | ESC: Salir", True, GRAY)
            self.screen.blit(controls, (20, SCREEN_HEIGHT - 30))
            
            # Mensaje de ayuda para la llave de prueba
            if self.player_keys < 3:
                hint = self.small_font.render("Ve a la esquina inferior derecha para recoger llaves (E)", True, CYAN)
                self.screen.blit(hint, (20, SCREEN_HEIGHT - 55))
            
    def show_game_over(self):
        """Mostrar pantalla de Game Over"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, RED)
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(game_over_text, game_over_rect)
        
        restart_text = self.small_font.render("Press R to restart or ESC to quit", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        
        # Esperar input del usuario
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.player_health = 100
                        self.player_keys = 0
                        self.player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
                        waiting = False
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
                        
    def show_victory(self):
        """Mostrar pantalla de Victoria"""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        victory_text = self.font.render("VICTORY!", True, GREEN)
        victory_rect = victory_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(victory_text, victory_rect)
        
        credits_text = self.small_font.render("Has derrotado a los dinosaurios y escapado!", True, YELLOW)
        credits_rect = credits_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(credits_text, credits_rect)
        
        thanks_text = self.small_font.render("Press ESC to exit", True, WHITE)
        thanks_rect = thanks_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
        self.screen.blit(thanks_text, thanks_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                    waiting = False

if __name__ == "__main__":
    print("Iniciando Stomber Bomber...")
    print("Controles: WASD para mover, E para recoger llaves")
    print("Ve a la esquina inferior derecha para recoger las llaves (prueba)")
    game = StomberBomber()
    game.run()