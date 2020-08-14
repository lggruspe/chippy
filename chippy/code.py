import random
import sys

from .errors import ChippyError

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

def dispatch(instruction, impl):
    """Run instruction on implementation."""

    opcode = instruction >> 12
    x = (instruction & 0xf00) >> 8
    y = (instruction & 0xf0) >> 4
    nnn = instruction & 0xfff
    kk = instruction & 0xff
    funct = instruction & 0xf

    if opcode == 0:
        if kk == 0xe0:
            return impl.op_00e0()
        elif kk == 0xee:
            return impl.op_00ee()
    elif opcode == 1:
        return impl.op_1nnn(nnn)
    elif opcode == 2:
        return impl.op_2nnn(nnn)
    elif opcode == 3:
        return impl.op_3xkk(x, kk)
    elif opcode == 4:
        return impl.op_4xkk(x, kk)
    elif opcode == 5:
        if funct == 0:
            return impl.op_5xy0(x, y)
    elif opcode == 6:
        return impl.op_6xkk(x, kk)
    elif opcode == 7:
        return impl.op_7xkk(x, kk)
    elif opcode == 8:
        if 0 <= funct <= 7:
            return {
                0: lambda: impl.op_8xy0(x, y),
                1: lambda: impl.op_8xy1(x, y),
                2: lambda: impl.op_8xy2(x, y),
                3: lambda: impl.op_8xy3(x, y),
                4: lambda: impl.op_8xy4(x, y),
                5: lambda: impl.op_8xy5(x, y),
                6: lambda: impl.op_8xy6(x, y),
                7: lambda: impl.op_8xy7(x, y),
            }[funct]()
        elif funct == 0xe:
            return impl.op_8xye(x, y)
    elif opcode == 9:
        if funct == 0:
            return impl.op_9xy0(x, y)
    elif opcode == 0xa:
        return impl.op_annn(nnn)
    elif opcode == 0xb:
        return impl.op_bnnn(nnn)
    elif opcode == 0xc:
        return impl.op_cxkk(x, kk)
    elif opcode == 0xd:
        n = funct
        return impl.op_dxyn(x, y, n)
    elif opcode == 0xe:
        if kk == 0x9e:
            return impl.op_ex9e(x)
        elif kk == 0xa1:
            return impl.op_exa1(x)
    elif opcode == 0xf:
        case = {
            0x07: lambda: impl.op_fx07(x),
            0x0a: lambda: impl.op_fx0a(x),
            0x15: lambda: impl.op_fx15(x),
            0x18: lambda: impl.op_fx18(x),
            0x1e: lambda: impl.op_fx1e(x),
            0x29: lambda: impl.op_fx29(x),
            0x33: lambda: impl.op_fx33(x),
            0x55: lambda: impl.op_fx55(x),
            0x65: lambda: impl.op_fx65(x),
        }.get(kk)
        if case:
            return case()
    return ChippyError(f"Invalid instruction: {instruction:#06x}")
