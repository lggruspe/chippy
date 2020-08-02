"""chippy subprograms."""
from pathlib import Path
import errno
import sys

from .chippy import Chippy
from .config import Config
from .debug import Disassembler

def list_roms():
    """List avaiable ROMs."""
    roms = Path(__file__).parent.joinpath("roms")
    for rom in roms.glob('*'):
        print(rom.name)

def find_rom(program):
    """Find ROM in current directory or in ROMs directory."""
    rom = Path(program)
    if rom.is_file():
        return rom
    rom = Path(__file__).parent.joinpath("roms", program)
    if rom.is_file():
        return rom

def run(program, config=Config()):
    """Run chip-8 program."""
    rom = find_rom(program)
    if rom is None:
        print(f"Program '{program}' not found.", file=sys.stderr)
        sys.exit(errno.ENOENT)
    chippy = Chippy(config)
    chippy.load(rom)
    chippy.run()

def disassemble(program):
    """Disassemble chip-8 program."""
    rom = find_rom(program)
    if rom is None:
        print(f"Program '{program}' not found.", file=sys.stderr)
        sys.exit(errno.ENOENT)
    Disassembler.run(rom)
