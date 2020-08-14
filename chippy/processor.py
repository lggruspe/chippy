import random

class ExecutionUnit:
    def __init__(self, chip8):
        self.vm = chip8

    def op_0nnn(self, nnn):
        """Jump to routine at nnn."""
        raise NotImplementedError

    def op_00e0(self):
        """Clear chip8 display."""
        self.vm.initialize_display()

    def op_00ee(self):
        """Return from subroutine."""
        self.vm.stack_pointer -= 1
        self.vm.jump(self.vm.stack[self.vm.stack_pointer])

    def op_1nnn(self, nnn):
        """Jump to location nnn."""
        self.vm.jump(nnn)

    def op_2nnn(self, nnn):
        """Call subroutine at nnn."""
        self.vm.stack[self.vm.stack_pointer] = self.vm.program_counter
        self.vm.stack_pointer += 1
        self.vm.jump(nnn)

    def op_3xkk(self, x, kk):
        """Skip the next instruction if Vx == kk."""
        if self.vm.registers[x] == kk:
            self.vm.increment()

    def op_4xkk(self, x, kk):
        """Skip next instruction if Vx != kk."""
        if self.vm.registers[x] != kk:
            self.vm.increment()

    def op_5xy0(self, x, y):
        """Skip next instruction if Vx = Vy."""
        if self.vm.registers[x] == self.vm.registers[y]:
            self.vm.increment()

    def op_6xkk(self, x, kk):
        """Put kk into Vx."""
        self.vm.registers[x] = kk

    def op_7xkk(self, x, kk):
        """Add kk to Vx."""
        self.vm.registers[x] = (self.vm.registers[x] + kk) & 0xff

    def op_8xy0(self, x, y):
        """Set Vx = Vy."""
        self.vm.registers[x] = self.vm.registers[y]

    def op_8xy1(self, x, y):
        """Set Vx = Vx OR Vy."""
        self.vm.registers[x] |= self.vm.registers[y]

    def op_8xy2(self, x, y):
        """Set Vx = Vx AND Vy."""
        self.vm.registers[x] &= self.vm.registers[y]

    def op_8xy3(self, x, y):
        """Set Vx = Vx XOR Vy."""
        self.vm.registers[x] ^= self.vm.registers[y]

    def op_8xy4(self, x, y):
        """Add Vy to Vx and set Vf to the carry bit."""
        assert x != 0xf
        total = self.vm.registers[x] + self.vm.registers[y]
        self.vm.registers[x] = total & 0xff
        self.vm.registers[0xf] = int(total > 0xff)

    def op_8xy5(self, x, y):
        """Subtract Vy from Vx and set Vf to 1 if there's no borrow."""
        assert x != 0xf
        difference = self.vm.registers[x] - self.vm.registers[y]
        self.vm.registers[x] = difference & 0xff
        self.vm.registers[0xf] = int(difference > 0)   # or >= 0? (see Cowgod reference)

    def op_8xy6(self, x, y):
        """Set Vx = Vx >> 1, and set Vf to the LSB prior to the shift.

        NOTE Descriptions differ between
        - http://mattmik.com/files/chip8/mastering/chip8.html
        - http://devernay.free.fr/hacks/chip8/C8TECH10.HTM

        Vx should be shifted, not Vy.
        Vy should be ignored.
        """
        assert x != 0xf
        y = x
        self.vm.registers[0xf] = self.vm.registers[y] & 0x01
        self.vm.registers[x] = self.vm.registers[y] >> 1

    def op_8xy7(self, x, y):
        """Set Vx = Vy - Vx and set Vf to 1 if there's no borrow."""
        assert x != 0xf
        difference = self.vm.registers[y] - self.vm.registers[x]
        self.vm.registers[x] = difference & 0xff
        self.vm.registers[0xf] = int(difference > 0)   # or >= 0?

    def op_8xye(self, x, y):
        """Set Vx = Vy << 1, and set Vf to the MSB prior to the shift.

        NOTE Descriptions differ between
        - http://mattmik.com/files/chip8/mastering/chip8.html
        - http://devernay.free.fr/hacks/chip8/C8TECH10.HTM
        """
        # NOTE should Vx or Vy be shifted? (see op_8xy6)
        assert x != 0xf
        y = x
        self.vm.registers[0xf] = (self.vm.registers[y] >> 7) & 0x01
        self.vm.registers[x] = (self.vm.registers[y] << 1) & 0xff

    def op_9xy0(self, x, y):
        """Skip next instruction if Vx != Vy."""
        if self.vm.registers[x] != self.vm.registers[y]:
            self.vm.increment()

    def op_annn(self, nnn):
        """Set I to nnn."""
        self.vm.I = nnn

    def op_bnnn(self, nnn):
        """Jump to nnn + V0."""
        self.vm.jump((nnn + self.vm.registers[0]) & 0xfff)

    def op_cxkk(self, x, kk):
        """Set Vx = random byte & kk."""
        self.vm.registers[x] = random.randint(0x00, 0xff) & kk

    def op_dxyn(self, x, y, nibble):
        """Display n-byte sprite starting at memory location I at (Vx, Vy).

        The sprite is 8 pixels wide and n pixels tall.
        Set Vf = 1 iff any set pixels are unset.
        The sprite is drawn by XORing it with the display.

        Out of screen parts of sprites wrap around to the other side.
        """
        sprite = self.vm.ram[self.vm.I:self.vm.I + nibble]
        X = self.vm.registers[x] & 0x3f
        Y = self.vm.registers[y]
        self.vm.registers[0xf] = 0

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
            xor = self.vm.display[Y32] ^ shifted_row
            unset = self.vm.display[Y32] & shifted_row
            self.vm.display[Y32] = xor

            if shift_amount < 0:
                offscreen = unset >> (64 + shift_amount)
                unset <<= -shift_amount
                unset |= offscreen
            else:
                unset >>= shift_amount
            unset &= 0xff
            self.vm.registers[0xf] |= unset
        self.vm.registers[0xf] = 1 if self.vm.registers[0xf] else 0

    def op_ex9e(self, x):
        """Skip next instruction if key with the value of Vx is pressed."""
        pressed = (self.vm.keypad >> (self.vm.registers[x] & 0xf)) & 0x1
        if pressed:
            self.vm.increment()

    def op_exa1(self, x):
        """Skip next instruction if key with the value of Vx is not pressed."""
        pressed = (self.vm.keypad >> (self.vm.registers[x] & 0xf)) & 0x1
        if not pressed:
            self.vm.increment()

    def op_fx07(self, x):
        """Set Vx to the delay timer value."""
        self.vm.registers[x] = self.vm.delay_timer

    def op_fx0a(self, x):
        """Wait for a key press and store the value of the key in Vx."""
        self.vm.waiting.append(x)

    def op_fx15(self, x):
        """Set the delay timer to Vx."""
        self.vm.delay_timer = self.vm.registers[x]

    def op_fx18(self, x):
        """Set the sound timer to Vx."""
        self.vm.sound_timer = self.vm.registers[x]

    def op_fx1e(self, x):
        """Add Vx to I."""
        self.vm.I = (self.vm.I + self.vm.registers[x]) & 0xffff

    def op_fx29(self, x):
        """Set I to location of sprite for digit in Vx."""
        self.vm.I = (self.vm.registers[x] & 0x0f) * 5

    def op_fx33(self, x):
        """Store the BCD representation of Vx in memory locations I, I+1 and I+2."""
        b = self.vm.registers[x] // 100
        c = (self.vm.registers[x] // 10) % 10
        d = self.vm.registers[x] % 10
        self.vm.ram[self.vm.I] = b
        self.vm.ram[self.vm.I+1] = c
        self.vm.ram[self.vm.I+2] = d

    def op_fx55(self, x):
        """Store registers V0 to Vx (inclusive) in memory starting at location I.

        The value of I doesn't get incremented, unlike what the ff. guide says.
        - http://mattmik.com/files/chip8/mastering/chip8.html
        """
        self.vm.ram[self.vm.I:self.vm.I + x+1] = self.vm.registers[:x+1]

    def op_fx65(self, x):
        """Read registers V0 through Vx (inclusive) from memory starting at I.

        The value of I doesn't get incremented, unlike what the ff. guide says.
        - http://mattmik.com/files/chip8/mastering/chip8.html
        """
        self.vm.registers[:x+1] = self.vm.ram[self.vm.I:self.vm.I + x + 1]
