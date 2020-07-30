from . import Chippy
import sys

if __name__ == "__main__":
    chip = Chippy()
    if len(sys.argv) > 1:
        chip.load(sys.argv[1])
    chip.run()
