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
