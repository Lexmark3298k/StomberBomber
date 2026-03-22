"""
Stomber Bomber - Configuración del juego
"""

import pygame

# Configuración de pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 50
FPS = 60
WINDOW_TITLE = "STOMBER BOMBER - Jurassic Mayhem"

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
DARK_GREEN = (0, 100, 0)
DARK_RED = (139, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)

# Colores específicos
LASER_COLOR = (255, 50, 50)
BUTTON_COLOR = (100, 100, 255)
RAPTOR_COLOR = (150, 150, 255)
HIDING_COLOR = (139, 69, 19)
BOSS_COLOR = (30, 30, 30)
HEALTH_BAR_COLOR = (255, 0, 0)
HEALTH_BG_COLOR = (64, 0, 0)

# Velocidades
PLAYER_SPEED = 5
PLAYER_SHOT_COOLDOWN = 20  # frames

PATROL_SPEED = 2
CHASE_SPEED = 4
BOSS_SPEED = 2

# Sistema de visión
VISION_RANGE = 300
VISION_ANGLE = 90

# Datos iniciales del jugador
PLAYER_START_HEALTH = 100
PLAYER_START_KEYS = 0
PLAYER_START_AMMO = 30

# Configuración de niveles
LEVELS = {
    1: "Salon 1: Carnicería Cretácica",
    2: "Salon 2: Sala de los Ecos",
    3: "Salon 3: Muro de la Muerte",
    4: "Salon 4: Estática Mortal",
    5: "Salon 5: Danza con Dante"
}

# Rutas de assets
FONT_PATH = "assets/fonts/press_start.ttf"
SOUNDS_PATH = "assets/sounds/"
SPRITES_PATH = "assets/sprites/"

def init_pygame():
    """Inicializa pygame y devuelve la pantalla"""
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(WINDOW_TITLE)
    return screen