"""Chip8 display."""

import pygame

def draw_pixel(x, y, scale=1):
    """Draw pixel on the display."""
    surface = pygame.display.get_surface()
    rect = pygame.Rect(x * scale, y * scale, scale, scale)
    color = pygame.Color(255, 255, 255)
    pygame.draw.rect(surface, color, rect)

class Display:
    def __init__(self, chip8):
        self.width = 64
        self.height = 32
        self.scale = 12

        self.chip8 = chip8
        self.running = True

    @property
    def screen_size(self):
        """Get screen size."""
        return (self.width * self.scale, self.height * self.scale)

    def render(self):
        """Render chip8 sprites."""
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        for y, row in enumerate(self.chip8.display):
            x = 0
            bits = row
            while bits:
                cell = 0x8000000000000000 & bits
                if cell:
                    draw_pixel(x, y, self.scale)
                bits &= 0x7fffffffffffffff
                bits <<= 1
                x += 1
        pygame.display.update()

    def init_screen(self):
        """Initialize screen."""
        pygame.init()
        pygame.display.set_caption("Chippy")
        self.screen = pygame.display.set_mode(self.screen_size)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
