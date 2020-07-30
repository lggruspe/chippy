"""Chip8 keypad module."""

import sys

from pynput import keyboard

def to_number(s):
    """Convert one-hexdigit hexstring or KeyCode to number."""
    try:
        if isinstance(s, str):
            return int(s, 16) & 0xf
        if isinstance(s, keyboard.KeyCode):
            return int(s.char, 16) & 0xf
    except ValueError:
        pass

def wait_keypress():
    """Wait for hex keypress."""
    key = to_number(input("[press key] "))
    while key is None:
        key = to_number(input("[press key] "))
    return key

def listen(chip8):
    """Non-blocking chip8 keypad listener."""
    def on_press(key):
        shift_amount = to_number(key)
        if shift_amount is None:
            return
        mask = 1 << shift_amount
        chip8.keypad |= mask

    def on_release(key):
        shift_amount = to_number(key)
        if shift_amount is None:
            return
        left = 0xffff
        right = (1 << (shift_amount + 1)) - 1
        mask = left - (right >> 1)
        chip8.keypad &= mask

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
