"""Game constants and configuration settings."""

# Window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Space Shooter"

# ============================================================
# VIBRANT COLOR PALETTE
# ============================================================

# Background / Space
DARK_BLUE = "#0B0D2E"       # Deep space blue background
MEDIUM_BLUE = "#1A1F4E"     # Slightly lighter blue for panels
DARK_PURPLE = "#0D0A25"     # Canvas background alternative

# Core Colors
WHITE = "#FFFFFF"
BLACK = "#000000"
DARK_GRAY = "#333333"
LIGHT_GRAY = "#888888"

# Vibrant Accents
GOLD = "#FFD700"            # Score / important text
AMBER = "#FFC107"           # Secondary accent
HOT_PINK = "#FF1493"        # Lives display
NEON_CYAN = "#00FFE5"       # Player ship color
BRIGHT_GREEN = "#39FF14"    # Bullet color
NEON_YELLOW = "#E5FF00"     # Star accent
ELECTRIC_BLUE = "#4169E1"   # Highlight

# Classic Colors (kept for compatibility, but overridden with vibrant ones)
RED = "#FF0040"             # Brighter red
GREEN = "#00FF87"           # Neon green
BLUE = "#0099FF"            # Bright blue
YELLOW = "#FFD700"          # Gold (same as GOLD)
CYAN = NEON_CYAN            # Use neon cyan
MAGENTA = "#FF00AA"         # Pinkish magenta
ORANGE = "#FF6600"          # Bright orange

# HUD Panel Colors
HUD_BG_COLOR = "#0A0C2A"   # Semi-transparent dark blue for HUD backgrounds
HUD_BORDER_COLOR = "#2A2F6E"  # Border color for HUD panels
HUD_SHADOW_COLOR = "#05061A"  # Shadow/outline color for text

# ============================================================
# PLAYER SETTINGS
# ============================================================
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_COLOR = NEON_CYAN
PLAYER_OUTLINE = WHITE
PLAYER_SPEED = 5
PLAYER_START_X = WINDOW_WIDTH // 2
PLAYER_START_Y = WINDOW_HEIGHT - 60
PLAYER_MAX_LIVES = 3

# ============================================================
# BULLET SETTINGS
# ============================================================
BULLET_WIDTH = 6
BULLET_HEIGHT = 18
BULLET_COLOR = BRIGHT_GREEN
BULLET_OUTLINE = "#00CC00"
BULLET_SPEED = -10  # Negative = upward (slightly faster)
BULLET_COOLDOWN = 200  # milliseconds between shots (slightly faster)

# ============================================================
# ENEMY SETTINGS
# ============================================================
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 30
ENEMY_COLOR = RED
ENEMY_SPEED = 3
ENEMY_SPAWN_INTERVAL = 1000  # milliseconds between enemy spawns
ENEMY_MOVE_DOWN_AMOUNT = 20  # pixels to move down when hitting edge
ENEMY_COLORS = [
    "#FF0040",  # Vibrant Red
    "#FF00AA",  # Hot Pink
    "#FF6600",  # Bright Orange
    "#FF4500",  # Orange Red
    "#DC143C",  # Crimson
    "#FF1493",  # Deep Pink
]

# ============================================================
# STAR FIELD SETTINGS
# ============================================================
STAR_COUNT = 150            # More stars for richer background
STAR_MIN_SIZE = 1
STAR_MAX_SIZE = 3
STAR_SPEED = 1
STAR_COLORS = [
    "#FFFFFF",  # White
    "#B0E0FF",  # Light blue
    "#E6F0FF",  # Pale blue
    "#FFFACD",  # Lemon chiffon
    "#FFE4B5",  # Moccasin (warm)
    "#E0FFFF",  # Light cyan
]

# ============================================================
# SCORING / HUD
# ============================================================
SCORE_PER_ENEMY = 100
SCORE_FONT_SIZE = 36            # Larger and clearer
LIVES_FONT_SIZE = 28            # Larger lives display
GAME_OVER_FONT_SIZE = 56        # Bigger game over
RESTART_FONT_SIZE = 24          # Bigger restart prompt
HUD_FONT = "Arial"              # Font family for HUD
HUD_PANEL_PADDING = 15          # Padding for HUD panels

# ============================================================
# GAME FRAME RATE
# ============================================================
FPS = 60

