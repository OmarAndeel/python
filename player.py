"""Player spaceship class."""

import tkinter as tk
from constants import *


class Player:
    """Represents the player's spaceship."""

    def __init__(self, canvas):
        self.canvas = canvas
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_MAX_LIVES
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1500  # milliseconds
        self.blink_visible = True
        self.blink_timer = 0

        # Create the spaceship shape using a polygon
        self.create_shape()

    def create_shape(self):
        """Draw the player spaceship as a triangle (arrow shape)."""
        x1 = self.x - self.width // 2
        y1 = self.y + self.height // 2
        x2 = self.x + self.width // 2
        y2 = self.y + self.height // 2
        x3 = self.x
        y3 = self.y - self.height // 2

        self.shape = self.canvas.create_polygon(
            x1, y1, x2, y2, x3, y3,
            fill=PLAYER_COLOR,
            outline=WHITE,
            width=2,
            tags="player"
        )

    def move_left(self):
        """Move the player left."""
        if self.x - self.width // 2 > 0:
            self.x -= self.speed
            self.canvas.move(self.shape, -self.speed, 0)

    def move_right(self):
        """Move the player right."""
        if self.x + self.width // 2 < WINDOW_WIDTH:
            self.x += self.speed
            self.canvas.move(self.shape, self.speed, 0)

    def get_bullet_spawn_position(self):
        """Return (x, y) where bullets should spawn from."""
        return self.x, self.y - self.height // 2

    def hit(self):
        """Handle being hit by an enemy."""
        if not self.invulnerable:
            self.lives -= 1
            if self.lives > 0:
                self.make_invulnerable(self.invulnerable_duration)
            return True
        return False

    def make_invulnerable(self, duration_ms):
        """Make player invulnerable for a duration (blinking effect)."""
        self.invulnerable = True
        self.invulnerable_timer = duration_ms
        self.blink_timer = 0
        self.blink_visible = True

    def update(self, dt_ms):
        """Update invulnerability state."""
        if self.invulnerable:
            self.invulnerable_timer -= dt_ms
            self.blink_timer += dt_ms

            # Blink every 100ms
            if self.blink_timer >= 100:
                self.blink_timer = 0
                self.blink_visible = not self.blink_visible
                if self.blink_visible:
                    self.canvas.itemconfig(self.shape, state="normal")
                else:
                    self.canvas.itemconfig(self.shape, state="hidden")

            if self.invulnerable_timer <= 0:
                self.invulnerable = False
                self.canvas.itemconfig(self.shape, state="normal")

    def respawn(self):
        """Respawn the player at the starting position."""
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.canvas.coords(
            self.shape,
            self.x - self.width // 2, self.y + self.height // 2,
            self.x + self.width // 2, self.y + self.height // 2,
            self.x, self.y - self.height // 2
        )
        self.make_invulnerable(2000)  # 2 seconds of invulnerability after respawn

    def destroy(self):
        """Remove the player from the canvas."""
        self.canvas.delete(self.shape)

