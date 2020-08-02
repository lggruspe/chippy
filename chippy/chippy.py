"""Chip8 interpreter."""

import array
import pathlib
import time

from .code import classify, handle_instruction, InstructionSet
from .debug import Disassembler
from .errors import ChippyError
from .window import Window

class Chippy:
    def __init__(self):
        """Initialize RAM, registers, stack, IO and sprite data."""
        self.ram = bytearray([0x00] * 4096)

        self.registers = bytearray([0x00] * 16)
        self.I = 0x0000
        self.sound_timer = 0x00
        self.delay_timer = 0x00
        self.program_counter = 0x0200
        self.stack_pointer = 0x00
        self.stack = array.array('H', [0x0000] * 16)

        self.keypad = 0x0000
        self.display = None
        # 64-by-32 display

        self.initialize_display()
        self.initialize_sprite_data()

        self.running = False
        self.waiting = []

    def initialize_display(self):
        """Clear display."""
        self.display = array.array('Q', [0x0000000000000000] * 32)

    def initialize_sprite_data(self):
        """Initialize sprite data in locates 0x000 to 0x050."""
        self.ram[:5]    = (0xf0, 0x90, 0x90, 0x90, 0xf0)
        self.ram[5:10]  = (0x20, 0x60, 0x20, 0x20, 0x70)
        self.ram[10:15] = (0Xf0, 0x10, 0xf0, 0x80, 0xf0)
        self.ram[15:20] = (0xf0, 0x10, 0xf0, 0x10, 0xf0)
        self.ram[20:25] = (0x90, 0x90, 0xf0, 0x10, 0x10)
        self.ram[25:30] = (0xf0, 0x80, 0xf0, 0x10, 0xf0)
        self.ram[30:35] = (0xf0, 0x80, 0xf0, 0x90, 0xf0)
        self.ram[35:40] = (0xf0, 0x10, 0x20, 0x40, 0x40)
        self.ram[40:45] = (0xf0, 0x90, 0xf0, 0x90, 0xf0)
        self.ram[45:50] = (0xf0, 0x90, 0xf0, 0x10, 0xf0)
        self.ram[50:55] = (0xf0, 0x90, 0xf0, 0x90, 0x90)
        self.ram[55:60] = (0xe0, 0x90, 0xe0, 0x90, 0xe0)
        self.ram[60:65] = (0xf0, 0x80, 0x80, 0x80, 0xf0)
        self.ram[65:70] = (0xe0, 0x90, 0x90, 0x90, 0xe0)
        self.ram[70:75] = (0xf0, 0x80, 0xf0, 0x80, 0xf0)
        self.ram[75:80] = (0xf0, 0x80, 0xf0, 0x80, 0x80)

    def jump(self, target):
        """Jump to target location."""
        if target < 0x200 or target >= len(self.ram):
            raise ChippyError(f"Invalid jump target: {target:#05x}")
        self.program_counter = target

    def buzz(self):
        """Sound buzzer."""

    def load(self, program: pathlib.Path):
        """Load program into address 0x200."""
        binary = program.read_bytes()
        size = len(binary)
        if size >= len(self.ram) - 0x200:
            raise ChippyError("Ran out of memory.")
        self.ram[0x200:size + 0x200] = binary

    def fetch(self):
        """Fetch current instruction."""
        msb = self.ram[self.program_counter]
        lsb = self.ram[self.program_counter + 1]
        return (msb << 8) | lsb

    def increment(self):
        """Increment program counter.

        This is called by instruction handlers.
        """
        self.program_counter += 2
        self.program_counter &= 0x0fff

    def execute(self, instruction):
        """Execute instruction."""
        handle_instruction(InstructionSet, instruction, self)

    def disassemble(self, instruction):
        """Disassemble instruction."""
        assembly = handle_instruction(Disassembler, instruction, self)
        print(assembly)

    def cycle(self):
        """Simulate one cycle."""
        instruction = self.fetch()
        self.increment()
        self.disassemble(instruction) #
        self.execute(instruction)

    def countdown(self):
        """Decrement timers and perform timer-related actions."""
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1
            self.buzz()

    def run(self):
        """Run program stored in memory."""
        self.running = True
        window = Window(self)
        window.init_screen()

        timer_60Hz = 0.01667
        while self.running:
            start_time = time.time()

            if not self.waiting:
                self.cycle()

            window.handle_events()
            window.render()

            cycle_duration = time.time() - start_time

            timer_60Hz -= cycle_duration
            if timer_60Hz <= 0:
                timer_60Hz = 0.01667
                self.countdown()

            remaining = 0.002 - cycle_duration
            if remaining > 0:
                time.sleep(remaining)