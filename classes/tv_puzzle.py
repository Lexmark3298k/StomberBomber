class TVPuzzle(pygame.sprite.Sprite):
    def __init__(self, x, y, color_sequence):
        self.sequence = color_sequence  # Lista de colores
        self.current_index = 0
        pass
    def interact(self, color):
        # Verificar si el color es correcto
        pass