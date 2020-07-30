"""Run chip8 interpreter."""

import sys

from . import Chippy

if __name__ == "__main__":
    chip = Chippy()
    if len(sys.argv) > 1:
        chip.load(sys.argv[1])
    chip.run()
