"""Chip-8 debugger."""

import pathlib

from .code import handle_instruction

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

class Disassembler:
    @staticmethod
    def op_0nnn(self, nnn):
        """Jump to routine at nnn."""
        return "nop"

    @staticmethod
    def op_00e0(self):
        """Clear chip8 display."""
        return "clear"

    @staticmethod
    def op_00ee(self):
        """Return from subroutine."""
        return "return"

    @staticmethod
    def op_1nnn(self, nnn):
        """Jump to location nnn."""
        return f"jump {nnn:#05x}"

    @staticmethod
    def op_2nnn(self, nnn):
        """Call subroutine at nnn."""
        return f"call {nnn:#05x}"

    @staticmethod
    def op_3xkk(self, x, kk):
        """Skip the next instruction if Vx == kk."""
        return f"skip if V{x:x} = {kk}"

    @staticmethod
    def op_4xkk(self, x, kk):
        """Skip next instruction if Vx != kk."""
        return f"skip if V{x:x} != {kk}"

    @staticmethod
    def op_5xy0(self, x, y):
        """Skip next instruction if Vx = Vy."""
        return f"skip if V{x:x} = V{y:x}"

    @staticmethod
    def op_6xkk(self, x, kk):
        """Put kk into Vx."""
        return f"V{x:x} = {kk}"

    @staticmethod
    def op_7xkk(self, x, kk):
        """Add kk to Vx."""
        return f"V{x:x} += {kk}"

    @staticmethod
    def op_8xy0(self, x, y):
        """Set Vx = Vy."""
        return f"V{x:x} = V{y:x}"

    @staticmethod
    def op_8xy1(self, x, y):
        """Set Vx = Vx OR Vy."""
        return f"V{x:x} |= V{y:x}"

    @staticmethod
    def op_8xy2(self, x, y):
        """Set Vx = Vx AND Vy."""
        return f"V{x:x} &= V{y:x}"

    @staticmethod
    def op_8xy3(self, x, y):
        """Set Vx = Vx XOR Vy."""
        return f"V{x:x} ^= V{y:x}"

    @staticmethod
    def op_8xy4(self, x, y):
        """Add Vy to Vx and set Vf to the carry bit."""
        return f"V{x:x} += V{y:x}, Vf = 'carry'"

    @staticmethod
    def op_8xy5(self, x, y):
        """Subtract Vy from Vx and set Vf to 1 if there's no borrow."""
        return f"V{x:x} -= V{y:x}, Vf = 'no borrow'"

    @staticmethod
    def op_8xy6(self, x, y):
        """Set Vx = Vy >> 1, and set Vf to the LSB prior to the shift.

        NOTE Descriptions differ between
        - http://mattmik.com/files/chip8/mastering/chip8.html
        - http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
        """
        return f"Vf = lsb V{y:x}\n\tV{x:x} = V{y:x} >> 1"

    @staticmethod
    def op_8xy7(self, x, y):
        """Set Vx = Vy - Vx and set Vf to 1 if there's no borrow."""
        return f"V{x:x} = V{y:x} - V{x:x}, Vf = 'no borrow'"

    @staticmethod
    def op_8xye(self, x, y):
        """Set Vx = Vy << 1, and set Vf to the MSB prior to the shift.

        NOTE Descriptions differ between
        - http://mattmik.com/files/chip8/mastering/chip8.html
        - http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
        """
        return f"Vf = msb V{y:x}\n\tV{x:x} = V{y:x} << 1"

    @staticmethod
    def op_9xy0(self, x, y):
        """Skip next instruction if Vx != Vy."""
        return f"skip if V{x:x} != V{y:x}"

    @staticmethod
    def op_annn(self, nnn):
        """Set I to nnn."""
        return f"I = {nnn:#05x}"

    @staticmethod
    def op_bnnn(self, nnn):
        """Jump to nnn + V0."""
        return f"jump V0 + {nnn:#05x}"

    @staticmethod
    def op_cxkk(self, x, kk):
        """Set Vx = random byte & kk."""
        return f"V{x:x} = random & {kk:#04x}"

    @staticmethod
    def op_dxyn(self, x, y, nibble):
        """Display n-byte sprite starting at memory location I at (Vx, Vy).

        The sprite is 8 pixels wide and n pixels tall.
        Set Vf = 1 iff any set pixels are unset.
        The sprite is drawn by XORing it with the display.
        """
        return f"display 8-by-{nibble} sprite at (V{x:x}, V{y:x})"

    @staticmethod
    def op_ex9e(self, x):
        """Skip next instruction if key with the value of Vx is pressed."""
        return f"skip if key @V{x:x} is pressed"

    @staticmethod
    def op_exa1(self, x):
        """Skip next instruction if key with the value of Vx is not pressed."""
        return f"skip if key @V{x:x} is not pressed"

    @staticmethod
    def op_fx07(self, x):
        """Set Vx to the delay timer value."""
        return f"V{x:x} = DT"

    @staticmethod
    def op_fx0a(self, x):
        """Wait for a key press and store the value of the key in Vx."""
        return f"V{x:x} = wait key"

    @staticmethod
    def op_fx15(self, x):
        """Set the delay timer to Vx."""
        return f"DT = V{x:x}"

    @staticmethod
    def op_fx18(self, x):
        """Set the sound timer to Vx."""
        return f"ST = V{x:x}"

    @staticmethod
    def op_fx1e(self, x):
        """Add Vx to I."""
        return f"I += V{x:x}"

    @staticmethod
    def op_fx29(self, x):
        """Set I to location of sprite for digit in Vx."""
        return f"I = sprite address of digit in V{x:x}"

    @staticmethod
    def op_fx33(self, x):
        """Store the BCD representation of Vx in memory locations I, I+1 and I+2."""
        return f"I[:2] = bcd of value in V{x:x}"

    @staticmethod
    def op_fx55(self, x):
        """Store registers V0 to Vx (inclusive) in memory starting at location I.

        The value of I gets incremented by x + 1 afterwards.
        """
        return f"I[:{x:x} + 1] = V[:{x:x} + 1]\n\tI += {x} + 1"

    @staticmethod
    def op_fx65(self, x):
        """Read registers V0 through Vx (inclusive) from memory starting at I.

        The value of I gets incremented by x + 1 afterwards.
        """
        return f"V[:{x:x} + 1] = I[:{x:x} + 1]\n\tI += {x} + 1"

    @staticmethod
    def run(program: pathlib.Path):
        """Disassemble chip-8 program file."""
        binary = program.read_bytes()
        for offset, byte in enumerate(binary):
            if offset % 2:
                continue
            next_byte = binary[offset + 1]
            instruction = (byte << 8) + next_byte
            assembly = handle_instruction(Disassembler, instruction, check=False)
            if assembly:
                print(f"{0x200+offset:#06x} {instruction:#06x} {assembly}")
            else:
                print(f"Invalid instruction: {instruction:#06x}")
