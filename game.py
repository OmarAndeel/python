"""Main game logic and loop."""

import tkinter as tk
import random
from constants import *
from player import Player
from enemy import Enemy
from bullet import Bullet


class SpaceShooterGame:
    """Main game class handling the game loop and state."""

    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.resizable(False, False)

        # Create main frame
        self.frame = tk.Frame(root, bg=BLACK)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas
        self.canvas = tk.Canvas(
            self.frame,
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            bg=BLACK,
            highlightthickness=0
        )
        self.canvas.pack()

        # Center the window on screen
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")

        # Game state
        self.running = False
        self.game_over = False
        self.score = 0
        self.last_bullet_time = 0
        self.last_enemy_spawn_time = 0
        self.last_frame_time = 0
        self.elapsed_time = 0

        # Game objects
        self.player = None
        self.bullets = []
        self.enemies = []
        self.stars = []
        self.keys_pressed = set()

        # UI elements
        self.score_text = None
        self.lives_text = None
        self.game_over_text = None
        self.restart_text = None
        self.title_text = None
        self.start_text = None

        # Create star field background
        self.create_star_field()

        # Show start screen
        self.show_start_screen()

        # Bind keyboard events
        self.canvas.bind_all("<KeyPress>", self.on_key_press)
        self.canvas.bind_all("<KeyRelease>", self.on_key_release)
        self.canvas.bind_all("<Button-1>", self.on_click)

        # Start the game loop
        self.last_frame_time = self.root.tk.call('clock', 'milliseconds')
        self.game_loop()

    def create_star_field(self):
        """Create a scrolling star field background."""
        for _ in range(STAR_COUNT):
            x = random.randint(0, WINDOW_WIDTH)
            y = random.randint(0, WINDOW_HEIGHT)
            size = random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)
            brightness = random.randint(100, 255)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"

            star = self.canvas.create_oval(
                x, y, x + size, y + size,
                fill=color,
                outline="",
                tags="star"
            )
            self.stars.append({
                "id": star,
                "x": x,
                "y": y,
                "size": size,
                "speed": random.uniform(0.5, 2.0)
            })

    def update_stars(self):
        """Scroll stars downward to create movement effect."""
        for star in self.stars:
            star["y"] += star["speed"] * STAR_SPEED
            self.canvas.move(star["id"], 0, star["speed"] * STAR_SPEED)

            # Wrap around to top
            if star["y"] > WINDOW_HEIGHT:
                star["y"] = -star["size"]
                star["x"] = random.randint(0, WINDOW_WIDTH)
                self.canvas.coords(
                    star["id"],
                    star["x"], star["y"],
                    star["x"] + star["size"],
                    star["y"] + star["size"]
                )

    def show_start_screen(self):
        """Display the title/start screen."""
        # Title
        self.title_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60,
            text="🚀 SPACE SHOOTER 🚀",
            fill=CYAN,
            font=("Arial", 36, "bold"),
            tags="ui"
        )

        # Subtitle
        subtitle = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2,
            text="Defend Earth from the alien invasion!",
            fill=LIGHT_GRAY,
            font=("Arial", 16),
            tags="ui"
        )

        # Instructions
        instructions = [
            "← → or A/D : Move left/right",
            "SPACE : Shoot",
            "ESC : Pause/Quit",
        ]
        y_pos = WINDOW_HEIGHT // 2 + 40
        for instruction in instructions:
            self.canvas.create_text(
                WINDOW_WIDTH // 2, y_pos,
                text=instruction,
                fill=WHITE,
                font=("Arial", 14),
                tags="ui"
            )
            y_pos += 25

        # Start prompt
        self.start_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 140,
            text="Click or press ENTER to start",
            fill=YELLOW,
            font=("Arial", 18, "bold"),
            tags="ui"
        )

        # Blinking effect for start text
        self.blink_start()

    def blink_start(self):
        """Blink the start prompt."""
        if self.start_text and not self.running and not self.game_over:
            current = self.canvas.itemcget(self.start_text, "fill")
            new_color = YELLOW if current == DARK_GRAY else DARK_GRAY
            try:
                self.canvas.itemconfig(self.start_text, fill=new_color)
            except tk.TclError:
                pass
            self.root.after(500, self.blink_start)

    def clear_ui(self):
        """Remove all UI elements."""
        self.canvas.delete("ui")

    def start_game(self):
        """Initialize and start the game."""
        self.clear_ui()
        self.running = True
        self.game_over = False
        self.score = 0
        self.elapsed_time = 0
        self.bullets = []
        self.enemies = []
        self.keys_pressed = set()
        self.last_bullet_time = 0
        self.last_enemy_spawn_time = 0

        # Create player
        self.player = Player(self.canvas)

        # Create HUD
        self.create_hud()

    def create_hud(self):
        """Create the heads-up display (score and lives)."""
        self.score_text = self.canvas.create_text(
            10, 10,
            anchor="nw",
            text=f"Score: {self.score}",
            fill=WHITE,
            font=("Arial", SCORE_FONT_SIZE, "bold"),
            tags="hud"
        )

        self.lives_text = self.canvas.create_text(
            WINDOW_WIDTH - 10, 10,
            anchor="ne",
            text=f"Lives: {self.player.lives}",
            fill=GREEN,
            font=("Arial", SCORE_FONT_SIZE, "bold"),
            tags="hud"
        )

    def update_hud(self):
        """Update the HUD display."""
        if self.score_text:
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
        if self.lives_text:
            self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.player.lives}")

    def show_game_over(self):
        """Display the game over screen."""
        self.running = False
        self.game_over = True

        # Remove HUD
        self.canvas.delete("hud")

        # Game over text
        self.game_over_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40,
            text="GAME OVER",
            fill=RED,
            font=("Arial", GAME_OVER_FONT_SIZE, "bold"),
            tags="ui"
        )

        # Final score
        self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10,
            text=f"Final Score: {self.score}",
            fill=WHITE,
            font=("Arial", 28, "bold"),
            tags="ui"
        )

        # Restart prompt
        self.restart_text = self.canvas.create_text(
            WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60,
            text="Click or press ENTER to play again",
            fill=YELLOW,
            font=("Arial", RESTART_FONT_SIZE, "bold"),
            tags="ui"
        )

        # Blinking effect
        self.blink_restart()

    def blink_restart(self):
        """Blink the restart prompt."""
        if self.restart_text and self.game_over:
            current = self.canvas.itemcget(self.restart_text, "fill")
            new_color = YELLOW if current == DARK_GRAY else DARK_GRAY
            try:
                self.canvas.itemconfig(self.restart_text, fill=new_color)
            except tk.TclError:
                pass
            self.root.after(500, self.blink_restart)

    def spawn_enemy(self):
        """Spawn a new enemy at the top of the screen."""
        enemy = Enemy(self.canvas)
        self.enemies.append(enemy)

    def spawn_bullet(self):
        """Spawn a bullet from the player's position."""
        if self.player:
            x, y = self.player.get_bullet_spawn_position()
            bullet = Bullet(self.canvas, x, y)
            self.bullets.append(bullet)

    def check_collisions(self):
        """Check and handle all collisions."""
        bullets_to_remove = []
        enemies_to_remove = []

        # Check bullet-enemy collisions
        for bullet in self.bullets[:]:
            if not bullet.active:
                continue

            bx1, by1, bx2, by2 = bullet.get_bounds()

            for enemy in self.enemies[:]:
                if not enemy.active:
                    continue

                ex1, ey1, ex2, ey2 = enemy.get_bounds()

                # Simple AABB collision detection
                if (bx1 < ex2 and bx2 > ex1 and by1 < ey2 and by2 > ey1):
                    # Collision detected!
                    bullet.destroy()
                    enemy.destroy()
                    self.score += SCORE_PER_ENEMY
                    self.create_explosion_effect(enemy.x, enemy.y)
                    break

        # Check player-enemy collisions
        if self.player:
            px1 = self.player.x - self.player.width // 2
            py1 = self.player.y - self.player.height // 2
            px2 = self.player.x + self.player.width // 2
            py2 = self.player.y + self.player.height // 2

            for enemy in self.enemies[:]:
                if not enemy.active:
                    continue

                ex1, ey1, ex2, ey2 = enemy.get_bounds()

                if (px1 < ex2 and px2 > ex1 and py1 < ey2 and py2 > ey1):
                    # Player hit!
                    enemy.destroy()
                    self.create_explosion_effect(enemy.x, enemy.y)
                    was_hit = self.player.hit()
                    if self.player.lives <= 0:
                        self.game_over = True

        # Clean up inactive objects
        self.bullets = [b for b in self.bullets if b.active]
        self.enemies = [e for e in self.enemies if e.active]

    def create_explosion_effect(self, x, y):
        """Create a simple explosion particle effect."""
        colors = [YELLOW, ORANGE, RED, WHITE]
        particles = []

        for _ in range(8):
            dx = random.randint(-15, 15)
            dy = random.randint(-15, 15)
            size = random.randint(2, 6)
            color = random.choice(colors)

            particle = self.canvas.create_oval(
                x + dx - size // 2, y + dy - size // 2,
                x + dx + size // 2, y + dy + size // 2,
                fill=color,
                outline="",
                tags="explosion"
            )
            particles.append(particle)

        # Remove explosion particles after a short delay
        self.root.after(300, lambda: self._clear_particles(particles))

    def _clear_particles(self, particles):
        """Remove explosion particle effects."""
        for particle in particles:
            try:
                self.canvas.delete(particle)
            except tk.TclError:
                pass

    def on_key_press(self, event):
        """Handle key press events."""
        self.keys_pressed.add(event.keysym)

        if event.keysym == "space" and self.running:
            self.spawn_bullet()

        if event.keysym == "Escape":
            if self.running:
                self.running = False
            else:
                self.root.quit()

        if event.keysym in ("Return", "KP_Enter"):
            if not self.running:
                if self.game_over:
                    self.reset_game()
                else:
                    self.start_game()

    def on_key_release(self, event):
        """Handle key release events."""
        self.keys_pressed.discard(event.keysym)

    def on_click(self, event):
        """Handle mouse click events."""
        if not self.running:
            if self.game_over:
                self.reset_game()
            else:
                self.start_game()

    def reset_game(self):
        """Reset the game state completely."""
        # Clean up existing objects
        self.canvas.delete("all")
        self.bullets = []
        self.enemies = []
        self.stars = []
        self.player = None
        self.score_text = None
        self.lives_text = None
        self.game_over_text = None
        self.restart_text = None
        self.title_text = None
        self.start_text = None

        # Recreate star field and start
        self.create_star_field()
        self.game_over = False
        self.start_game()

    def handle_input(self):
        """Process player input each frame."""
        if not self.player or not self.running:
            return

        if "Left" in self.keys_pressed or "a" in self.keys_pressed:
            self.player.move_left()
        if "Right" in self.keys_pressed or "d" in self.keys_pressed:
            self.player.move_right()

    def update(self, dt_ms):
        """Update all game objects."""
        if not self.running:
            return

        # Update stars (always)
        self.update_stars()

        # Update player
        if self.player:
            self.player.update(dt_ms)

        # Spawn enemies
        current_time = self.root.tk.call('clock', 'milliseconds')
        if current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_INTERVAL:
            self.spawn_enemy()
            self.last_enemy_spawn_time = current_time

        # Update enemies
        for enemy in self.enemies[:]:
            if not enemy.update():
                self.enemies.remove(enemy)

        # Update bullets
        for bullet in self.bullets[:]:
            if not bullet.update():
                self.bullets.remove(bullet)

        # Check collisions
        self.check_collisions()

        # Update HUD
        self.update_hud()

        # Update elapsed time
        self.elapsed_time += dt_ms

        # Check game over
        if self.game_over:
            self.show_game_over()

    def game_loop(self):
        """Main game loop called repeatedly."""
        current_time = self.root.tk.call('clock', 'milliseconds')
        dt_ms = current_time - self.last_frame_time
        self.last_frame_time = current_time

        # Cap delta time to prevent large jumps
        if dt_ms > 100:
            dt_ms = 16

        # Handle input and update game state
        self.handle_input()
        self.update(dt_ms)

        # Schedule next frame
        self.root.after(int(1000 / FPS), self.game_loop)

