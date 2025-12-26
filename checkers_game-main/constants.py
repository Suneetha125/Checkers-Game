WIDTH = 500
HEIGHT = 500
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS
FPS = 60

# Colors
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
RED = (200, 30, 30)
GREEN = (40, 180, 99)
GREY = (128, 128, 128)
HIGHLIGHT = (255, 215, 0)
SELECT = (65, 105, 225)

# Piece scoring
MAN_VAL = 100
KING_VAL = 175

# Directories
ASSETS_DIR = "assets"
IMAGES_DIR = ASSETS_DIR + "/images"
SOUNDS_DIR = ASSETS_DIR + "/sounds"

# Images
BOARD_IMAGE = IMAGES_DIR + "/board_wood.png"
PIECE_RED_IMG = IMAGES_DIR + "/piece_red.png"
PIECE_BLACK_IMG = IMAGES_DIR + "/piece_black.png"
CROWN_IMG = IMAGES_DIR + "/crown.png"

# Sounds
CLICK_SOUND = SOUNDS_DIR + "/click.wav"
MOVE_SOUND = SOUNDS_DIR + "/move.wav"
CAPTURE_SOUND = SOUNDS_DIR + "/capture.wav"

# Directions
UP_LEFT = (-1, -1)
UP_RIGHT = (-1, 1)
DOWN_LEFT = (1, -1)
DOWN_RIGHT = (1, 1)
