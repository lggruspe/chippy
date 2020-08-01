"""Run chip8 interpreter."""

from argparse import ArgumentParser

from . import app

if __name__ == "__main__":
    parser = ArgumentParser(prog="Chippy", description="Run chip-8 emulator.")
    parser.add_argument("-r", "--rom", help="load chip-8 ROM")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list available ROMs")
    args = parser.parse_args()

    if args.list:
        app.list_roms()
    elif args.rom:
        app.run(args.rom)
