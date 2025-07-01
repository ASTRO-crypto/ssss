"""
Game constants and configuration
"""

# Display settings
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# UI Colors
UI_BACKGROUND = (45, 45, 45)
UI_PANEL = (60, 60, 60)
UI_BUTTON = (80, 80, 80)
UI_BUTTON_HOVER = (100, 100, 100)
UI_TEXT = WHITE
UI_ACCENT = (0, 150, 255)

# Game settings
INITIAL_COUNTRIES = 8
MIN_COUNTRIES = 4
MAX_COUNTRIES = 12

# Economic constants
BASE_TAX_RATE = 0.15
MIN_TAX_RATE = 0.05
MAX_TAX_RATE = 0.50
BASE_GDP_GROWTH = 0.02

# Population constants
BASE_POPULATION_GROWTH = 0.01
MAX_POPULATION_GROWTH = 0.03
BASE_HAPPINESS = 50
MIN_HAPPINESS = 0
MAX_HAPPINESS = 100

# Government types
GOVERNMENT_TYPES = {
    'democracy': {
        'name': 'Democracy',
        'election_frequency': 4,  # years
        'corruption_resistance': 0.8,
        'stability_bonus': 0.1,
        'growth_modifier': 1.0
    },
    'monarchy': {
        'name': 'Monarchy',
        'election_frequency': 0,  # no elections
        'corruption_resistance': 0.5,
        'stability_bonus': 0.2,
        'growth_modifier': 0.9
    },
    'dictatorship': {
        'name': 'Dictatorship',
        'election_frequency': 0,  # no elections
        'corruption_resistance': 0.3,
        'stability_bonus': -0.1,
        'growth_modifier': 1.1
    },
    'republic': {
        'name': 'Republic',
        'election_frequency': 6,  # years
        'corruption_resistance': 0.7,
        'stability_bonus': 0.05,
        'growth_modifier': 1.05
    }
}

# Time constants
MONTHS_PER_YEAR = 12
DAYS_PER_MONTH = 30
GAME_SPEED_MULTIPLIER = 10  # Game days per real second