"""Chip-8 debugger."""

class Debugger:
    def __init__(self, chip8):
        self.chip8 = chip8
        self.PC = -1

    def print_info(self):
        """Print program counter and current instruction."""
        PC = self.chip8.program_counter
        if self.PC != PC:
            instruction = self.chip8.fetch()

            print(f"PC: {PC:#05x} {instruction:#06x}")
            self.PC = PC
