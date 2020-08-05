import random
import sys

from .errors import ChippyError

class InstructionSet:
    @staticmethod
    def op_0nnn(self, nnn):
        """Jump to routine at nnn."""
        raise NotImplementedError

    @staticmethod
    def op_00e0(self):
        """Clear chip8 display."""
        self.initialize_display()

    @staticmethod
    def op_00ee(self):
        """Return from subroutine."""
        self.stack_pointer -= 1
        self.jump(self.stack[self.stack_pointer])

    @staticmethod
    def op_1nnn(self, nnn):
        """Jump to location nnn."""
        self.jump(nnn)

    @staticmethod
    def op_2nnn(self, nnn):
        """Call subroutine at nnn."""
        self.stack[self.stack_pointer] = self.program_counter
        self.stack_pointer += 1
        self.jump(nnn)

    @staticmethod
    def op_3xkk(self, x, kk):
        """Skip the next instruction if Vx == kk."""
        if self.registers[x] == kk:
            self.increment()

    @staticmethod
    def op_4xkk(self, x, kk):
        """Skip next instruction if Vx != kk."""
        if self.registers[x] != kk:
            self.increment()

    @staticmethod
    def op_5xy0(self, x, y):
        """Skip next instruction if Vx = Vy."""
        if self.registers[x] == self.registers[y]:
            self.increment()

    @staticmethod
    def op_6xkk(self, x, kk):
        """Put kk into Vx."""
        self.registers[x] = kk

    @staticmethod
    def op_7xkk(self, x, kk):
        """Add kk to Vx."""
        self.registers[x] = (self.registers[x] + kk) & 0xff

    @staticmethod
    def op_8xy0(self, x, y):
        """Set Vx = Vy."""
        self.registers[x] = self.registers[y]

    @staticmethod
    def op_8xy1(self, x, y):
        """Set Vx = Vx OR Vy."""
        self.registers[x] |= self.registers[y]

    @staticmethod
    def op_8xy2(self, x, y):
        """Set Vx = Vx AND Vy."""
        self.registers[x] &= self.registers[y]

    @staticmethod
    def op_8xy3(self, x, y):
        """Set Vx = Vx XOR Vy."""
        self.registers[x] ^= self.registers[y]

    @staticmethod
    def op_8xy4(self, x, y):
        """Add Vy to Vx and set Vf to the carry bit."""
        total = self.registers[x] + self.registers[y]
        self.registers[0xf] = int(total > 0xff)
        self.registers[x] = total & 0xff

    @staticmethod
    def op_8xy5(self, x, y):
        """Subtract Vy from Vx and set Vf to 1 if there's no borrow."""
        self.registers[0xf] = int(self.registers[x] >= self.registers[y])
        self.registers[x] = (self.registers[x] - self.registers[y]) & 0xff

    @staticmethod
    def op_8xy6(self, x, y):
        """Set Vx = Vy >> 1, and set Vf to the LSB prior to the shift.

        NOTE Descriptions differ between
        - http://mattmik.com/files/chip8/mastering/chip8.html
        - http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
        """
        self.registers[0xf] = self.registers[y] & 0x01
        self.registers[x] = self.registers[y] >> 1

    @staticmethod
    def op_8xy7(self, x, y):
        """Set Vx = Vy - Vx and set Vf to 1 if there's no borrow."""
        self.registers[0xf] = int(self.registers[y] >= self.registers[x])
        self.registers[x] = (self.registers[y] - self.registers[x]) & 0xff

    @staticmethod
    def op_8xye(self, x, y):
        """Set Vx = Vy << 1, and set Vf to the MSB prior to the shift.

        NOTE Descriptions differ between
        - http://mattmik.com/files/chip8/mastering/chip8.html
        - http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
        """
        self.registers[0xf] = self.registers[y] >> 7
        self.registers[x] = (self.registers[y] << 1) & 0xff

    @staticmethod
    def op_9xy0(self, x, y):
        """Skip next instruction if Vx != Vy."""
        if self.registers[x] != self.registers[y]:
            self.increment()

    @staticmethod
    def op_annn(self, nnn):
        """Set I to nnn."""
        self.I = nnn

    @staticmethod
    def op_bnnn(self, nnn):
        """Jump to nnn + V0."""
        self.jump((nnn + self.registers[0]) & 0xfff)

    @staticmethod
    def op_cxkk(self, x, kk):
        """Set Vx = random byte & kk."""
        self.registers[x] = random.randint(0x00, 0xff) & kk

    @staticmethod
    def op_dxyn(self, x, y, nibble):
        """Display n-byte sprite starting at memory location I at (Vx, Vy).

        The sprite is 8 pixels wide and n pixels tall.
        Set Vf = 1 iff any set pixels are unset.
        The sprite is drawn by XORing it with the display.

        Out of screen parts of sprites wrap around to the other side.
        """
        sprite = self.ram[self.I:self.I + nibble]
        X = self.registers[x] & 0x3f
        Y = self.registers[y]
        self.registers[0xf] = 0

        shift_amount = 56 - X
        for i, row in enumerate(sprite):
            if shift_amount < 0:
                shifted_row = row >> -shift_amount
                offscreen = row << (64 + shift_amount)
                offscreen &= 0xffffffffffffffff
                shifted_row |= offscreen
            else:
                shifted_row = row << shift_amount

            Y32 = (Y + i) & 0x1f
            xor = self.display[Y32] ^ shifted_row
            unset = self.display[Y32] & shifted_row
            self.display[Y32] = xor

            if shift_amount < 0:
                offscreen = unset >> (64 + shift_amount)
                unset <<= -shift_amount
                unset |= offscreen
            else:
                unset >>= shift_amount
            unset &= 0xff
            self.registers[0xf] |= unset
        self.registers[0xf] = 1 if self.registers[0xf] else 0

    @staticmethod
    def op_ex9e(self, x):
        """Skip next instruction if key with the value of Vx is pressed."""
        pressed = (self.keypad >> (self.registers[x] & 0xf)) & 0x1
        if pressed:
            self.increment()

    @staticmethod
    def op_exa1(self, x):
        """Skip next instruction if key with the value of Vx is not pressed."""
        pressed = (self.keypad >> (self.registers[x] & 0xf)) & 0x1
        if not pressed:
            self.increment()

    @staticmethod
    def op_fx07(self, x):
        """Set Vx to the delay timer value."""
        self.registers[x] = self.delay_timer

    @staticmethod
    def op_fx0a(self, x):
        """Wait for a key press and store the value of the key in Vx."""
        self.waiting.append(x)

    @staticmethod
    def op_fx15(self, x):
        """Set the delay timer to Vx."""
        self.delay_timer = self.registers[x]

    @staticmethod
    def op_fx18(self, x):
        """Set the sound timer to Vx."""
        self.sound_timer = self.registers[x]

    @staticmethod
    def op_fx1e(self, x):
        """Add Vx to I."""
        self.I = (self.I + self.registers[x]) & 0xffff

    @staticmethod
    def op_fx29(self, x):
        """Set I to location of sprite for digit in Vx."""
        self.I = (self.registers[x] & 0x0f) * 5

    @staticmethod
    def op_fx33(self, x):
        """Store the BCD representation of Vx in memory locations I, I+1 and I+2."""
        b = self.registers[x] // 100
        c = (self.registers[x] // 10) % 10
        d = self.registers[x] % 10
        self.ram[self.I] = b
        self.ram[self.I+1] = c
        self.ram[self.I+2] = d

    @staticmethod
    def op_fx55(self, x):
        """Store registers V0 to Vx (inclusive) in memory starting at location I.

        The value of I doesn't get incremented, unlike what the ff. guide says.
        - http://mattmik.com/files/chip8/mastering/chip8.html
        """
        self.ram[self.I:self.I + x+1] = self.registers[:x+1]

    @staticmethod
    def op_fx65(self, x):
        """Read registers V0 through Vx (inclusive) from memory starting at I.

        The value of I doesn't get incremented, unlike what the ff. guide says.
        - http://mattmik.com/files/chip8/mastering/chip8.html
        """
        self.registers[:x+1] = self.ram[self.I:self.I + x + 1]

def classify(instruction):
    """Classify instruction.

    Return name of instruction handler and arguments.
    """
    if instruction in (0x00e0, 0x00ee):
        return f"op_{instruction:04x}",

    opcode = instruction >> 12

    if 0 <= opcode <= 2:
        return f"op_{opcode}nnn", instruction & 0x0fff
    if 3 <= opcode <= 4:
        x = instruction & 0x0f00
        kk = instruction & 0x00ff
        return f"op_{opcode}xkk", x >> 8, kk
    if opcode == 5:
        # if instruction & 0xf00f == 0x5000
        if instruction & 0x000f == 0:
            x = instruction & 0x0f00
            y = instruction & 0x00f0
            return "op_5xy0", x >> 8, y >> 4
    if 6 <= opcode <= 7:
        x = instruction & 0x0f00
        kk = instruction & 0x00ff
        return f"op_{opcode}xkk", x >> 8, kk
    if opcode == 8:
        function = instruction & 0x000f
        x = instruction & 0x0f00
        y = instruction & 0x00f0
        if 0 <= function <= 7:
            return f"op_8xy{function}", x >> 8, y >> 4
        if function == 0xe:
            return f"op_8xye", x >> 8, y >> 4
    if opcode == 9:
        if instruction & 0x000f == 0:
            x = instruction & 0x0f00
            y = instruction & 0x00f0
            return "op_9xy0", x >> 8, y >> 4
    if 0xa <= opcode <= 0xb:
        return f"op_{opcode:1x}nnn", instruction & 0x0fff
    if opcode == 0xc:
        x = instruction & 0x0f00
        kk = instruction & 0x00ff
        return "op_cxkk", x >> 8, kk
    if opcode == 0xd:
        x = instruction & 0x0f00
        y = instruction & 0x00f0
        n = instruction & 0x000f
        return "op_dxyn", x >> 8, y >> 4, n
    if opcode == 0xe:
        function = instruction & 0x00ff
        x = instruction & 0x0f00
        if function == 0x9e:
            return "op_ex9e", x >> 8
        if function == 0xa1:
            return "op_exa1", x >> 8
    if opcode == 0xf:
        function = instruction & 0x00ff
        if function in (0x07, 0x0a, 0x15, 0x18, 0x1e, 0x29, 0x33, 0x55, 0x65):
            x = instruction & 0x0f00
            return f"op_fx{function:02x}", x >> 8
    return "",

def handle_instruction(cls, instruction, chip8=None, *, check=True):
    """Handle instruction using static methods in cls."""
    name, *args = classify(instruction)
    if not name:
        if not check:
            return None
        message = f"Unknown instruction: {instruction:#06x}"
        print(message, file=sys.stderr)
        raise ChippyError(message)
    handler = getattr(cls, name)
    return handler(chip8, *args)
