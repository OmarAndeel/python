"""Game constants and configuration settings."""

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Space Shooter"

# Colors (RGB)
BLACK = "#000000"
WHITE = "#FFFFFF"
RED = "#FF0000"
GREEN = "#00FF00"
BLUE = "#0000FF"
YELLOW = "#FFFF00"
CYAN = "#00FFFF"
MAGENTA = "#FF00FF"
ORANGE = "#FFA500"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#888888"

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_COLOR = CYAN
PLAYER_SPEED = 5
PLAYER_START_X = WINDOW_WIDTH // 2
PLAYER_START_Y = WINDOW_HEIGHT - 60
PLAYER_MAX_LIVES = 3

# Bullet settings
BULLET_WIDTH = 4
BULLET_HEIGHT = 15
BULLET_COLOR = YELLOW
BULLET_SPEED = -8  # Negative = upward
BULLET_COOLDOWN = 250  # milliseconds between shots

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
ENEMY_COLOR = RED
ENEMY_SPEED = 3
ENEMY_SPAWN_INTERVAL = 1000  # milliseconds between enemy spawns
ENEMY_MOVE_DOWN_AMOUNT = 20  # pixels to move down when hitting edge

# Star field (background)
STAR_COUNT = 100
STAR_COLOR = WHITE
STAR_MIN_SIZE = 1
STAR_MAX_SIZE = 3
STAR_SPEED = 1

# Scoring
SCORE_PER_ENEMY = 100
SCORE_FONT_SIZE = 24
GAME_OVER_FONT_SIZE = 48
RESTART_FONT_SIZE = 20

# Game frame rate (updates per second)
FPS = 60

