"""Run chip8 interpreter."""

from argparse import ArgumentParser
import errno
import os.path
import sys

from . import Chippy

if __name__ == "__main__":
    parser = ArgumentParser(prog="Chippy", description="Run chip-8 emulator.")
    parser.add_argument("program", help="chip-8 ROM")
    args = parser.parse_args()
    if not os.path.isfile(args.program):
        print(f"Program '{args.program}' not found.", file=sys.stderr)
        sys.exit(errno.ENOENT)

    chip = Chippy()
    chip.load(args.program)
    chip.run()
