"""Run chip8 interpreter."""

from argparse import ArgumentParser

from . import app
from .config import Config

if __name__ == "__main__":
    config = Config()

    parser = ArgumentParser(prog="Chippy", description="Run chip-8 emulator.")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list available ROMs")
    parser.add_argument("-d", "--disassemble", metavar="ROM",
                        help="disassemble chip-8 program")
    parser.add_argument("-r", "--rom", help="load chip-8 ROM")
    parser.add_argument("-c", "--colors", default=config.color_scheme,
                        help=f"color scheme (default={config.color_scheme!r})")
    args = parser.parse_args()

    config.color_scheme = args.colors

    if args.list:
        app.list_roms()
    elif args.disassemble:
        app.disassemble(args.disassemble)
    elif args.rom:
        app.run(args.rom, config)
