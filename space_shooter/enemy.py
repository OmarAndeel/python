"""Enemy class representing alien ships."""

import random
import tkinter as tk
from constants import *


class Enemy:
    """Represents an enemy spaceship."""

    def __init__(self, canvas, x=None):
        self.canvas = canvas
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.speed = ENEMY_SPEED
        self.active = True
        self.direction = random.choice([-1, 1])  # -1 = left, 1 = right

        # Random x position, or use provided one
        if x is None:
            self.x = random.randint(self.width // 2, WINDOW_WIDTH - self.width // 2)
        else:
            self.x = x
        self.y = 0

        # Random color variation for enemies
        color = random.choice([RED, MAGENTA, ORANGE, "#FF6347", "#DC143C"])

        # Create enemy shape (alien-like UFO shape)
        self.create_shape(color)

    def create_shape(self, color):
        """Draw the enemy as a UFO-like shape."""
        x1 = self.x - self.width // 2
        y1 = self.y
        x2 = self.x + self.width // 2
        y2 = self.y + self.height

        # Main body (oval)
        self.shape = self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=color,
            outline=WHITE,
            width=1,
            tags="enemy"
        )

        # Dome on top
        dome_width = self.width // 3
        dome_height = self.height // 3
        self.dome = self.canvas.create_oval(
            self.x - dome_width // 2,
            self.y - dome_height // 2,
            self.x + dome_width // 2,
            self.y + dome_height // 2,
            fill=CYAN,
            outline=WHITE,
            width=1,
            tags="enemy"
        )

    def update(self):
        """Move the enemy downward and side to side."""
        # Move downward
        self.y += self.speed * 0.5

        # Move side to side (sinusoidal pattern)
        self.x += self.direction * self.speed * 0.3

        # Bounce off walls
        if self.x <= self.width // 2 or self.x >= WINDOW_WIDTH - self.width // 2:
            self.direction *= -1

        # Update canvas positions
        self.canvas.move(self.shape, 0, self.speed * 0.5)
        self.canvas.move(self.dome, 0, self.speed * 0.5)

        # Check if enemy is off-screen at bottom
        if self.y > WINDOW_HEIGHT + self.height:
            self.active = False
            self.canvas.delete(self.shape)
            self.canvas.delete(self.dome)
            return False
        return True

    def get_bounds(self):
        """Return bounding box for collision detection."""
        return (
            self.x - self.width // 2,
            self.y,
            self.x + self.width // 2,
            self.y + self.height
        )

    def destroy(self):
        """Remove the enemy from the canvas with a small explosion effect."""
        self.active = False
        # Simple explosion: flash white briefly, then delete
        self.canvas.itemconfig(self.shape, fill=WHITE)
        self.canvas.itemconfig(self.dome, fill=WHITE)
        self.canvas.after(50, self._cleanup)

    def _cleanup(self):
        """Delete the canvas items."""
        try:
            self.canvas.delete(self.shape)
            self.canvas.delete(self.dome)
        except tk.TclError:
            pass  # Already deleted

