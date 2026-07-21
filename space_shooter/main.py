"""Space Shooter - Entry Point

A classic arcade-style space shooter game built with Python and Tkinter.

Controls:
    - Left/Right Arrow or A/D: Move spaceship
    - SPACE: Shoot bullets
    - ESC: Quit game
    - Click or ENTER: Start / Restart game

Run this file to start the game.
"""

import tkinter as tk
import sys
import os

# Ensure we can import from the same directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from game import SpaceShooterGame


def main():
    """Initialize and run the Space Shooter game."""
    root = tk.Tk()
    game = SpaceShooterGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()

