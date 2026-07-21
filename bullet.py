"""Bullet / projectile class."""

import tkinter as tk
from constants import *


class Bullet:
    """Represents a bullet fired by the player."""

    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED
        self.active = True

        # Create bullet as a rectangle
        x1 = self.x - self.width // 2
        y1 = self.y - self.height // 2
        x2 = self.x + self.width // 2
        y2 = self.y + self.height // 2

        self.shape = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=BULLET_COLOR,
            outline="",
            tags="bullet"
        )

    def update(self):
        """Move the bullet upward. Returns False if off-screen."""
        self.y += self.speed
        self.canvas.move(self.shape, 0, self.speed)

        # Check if bullet is off-screen
        if self.y + self.height // 2 < 0:
            self.active = False
            self.canvas.delete(self.shape)
            return False
        return True

    def get_bounds(self):
        """Return bounding box for collision detection."""
        return (
            self.x - self.width // 2,
            self.y - self.height // 2,
            self.x + self.width // 2,
            self.y + self.height // 2
        )

    def destroy(self):
        """Remove the bullet from the canvas."""
        self.active = False
        self.canvas.delete(self.shape)

