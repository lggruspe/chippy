"""Chip8 display and keypad."""

import pygame

from .status import Mode

def press(chip8, key):
    """Press key on chip-8 keypad."""
    mask = 1 << key
    chip8.keypad |= mask

    # Handle op_fx0a
    if chip8.waiting:
        index = chip8.waiting.pop()
        chip8.registers[index] = key

def release(chip8, key):
    """Release key on chip-8 keypad."""
    mask = 0xffff
    mask -= (1 << key)
    chip8.keypad &= mask

KEYS = {
    pygame.K_x: 0,
    pygame.K_1: 1,
    pygame.K_2: 2,
    pygame.K_3: 3,
    pygame.K_q: 4,
    pygame.K_w: 5,
    pygame.K_e: 6,
    pygame.K_a: 7,
    pygame.K_s: 8,
    pygame.K_d: 9,
    pygame.K_z: 0xa,
    pygame.K_c: 0xb,
    pygame.K_4: 0xc,
    pygame.K_r: 0xd,
    pygame.K_f: 0xe,
    pygame.K_v: 0xf,
}
def convert_key(key):
    """Convert pygame key constant to chip-8 key input."""
    return KEYS.get(key)

def draw_pixel(x, y, scale=1, color=(255, 255, 255)):
    """Draw pixel on the display."""
    surface = pygame.display.get_surface()
    rect = pygame.Rect(x * scale, y * scale, scale, scale)
    pygame.draw.rect(surface, color, rect)

class Window:
    def __init__(self, chip8):
        self.width = 64
        self.height = 32
        self.scale = 12

        self.chip8 = chip8
        self.color_off = self.chip8.config.color_off
        self.color_on = self.chip8.config.color_on

    @property
    def screen_size(self):
        """Get screen size."""
        return (self.width * self.scale, self.height * self.scale)

    def render(self):
        """Render chip8 sprites."""
        self.screen.fill(self.color_off)
        for y, row in enumerate(self.chip8.display):
            x = 0
            bits = row
            while bits:
                cell = 0x8000000000000000 & bits
                if cell:
                    draw_pixel(x, y, self.scale, self.color_on)
                bits &= 0x7fffffffffffffff
                bits <<= 1
                x += 1
        pygame.display.update()

    def init_screen(self):
        """Initialize screen."""
        pygame.init()
        pygame.display.set_caption("Chippy")
        self.screen = pygame.display.set_mode(self.screen_size)

    def handle_key_event_when_running(self, event):
        """Handle KEYUP and KEYDOWN events in RUN mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SEMICOLON:
                self.chip8.status = Mode.PAUSE
                return
            key = convert_key(event.key)
            if key is not None:
                press(self.chip8, key)
        elif event.type == pygame.KEYUP:
            key = convert_key(event.key)
            if key is not None:
                release(self.chip8, key)

    def handle_key_event_when_paused(self, event):
        """Handle KEYUP and KEYDOWN events when paused."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.chip8.status = Mode.RUN
                return

    def handle_events(self):
        """Handle Pygame events and Chippy interrupts.."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.chip8.status = Mode.STOP
                return
            if self.chip8.status == Mode.RUN:
                self.handle_key_event_when_running(event)
            elif self.chip8.status == Mode.PAUSE:
                self.handle_key_event_when_paused(event)
