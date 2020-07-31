"""Chip8 keypad module."""

import sys

def to_number(s):
    """Convert one-hexdigit hexstring or KeyCode to number."""
    try:
        return int(s, 16) & 0xf
    except ValueError:
        pass
    except TypeError:
        pass

def wait_keypress():
    """Wait for hex keypress."""
    key = to_number(input("[press key] "))
    while key is None:
        key = to_number(input("[press key] "))
    return key

def press(chip8, key):
    shift_amount = to_number(key)
    if shift_amount is None:
        return
    mask = 1 << shift_amount
    chip8.keypad |= mask

def release(chip8, key):
    shift_amount = to_number(key)
    if shift_amount is None:
        return
    mask = 0xffff
    mask -= (1 << shift_amount)
    chip8.keypad &= mask
