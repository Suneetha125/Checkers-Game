from constants import ROWS, COLS

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def opponent(color):
    return "black" if color == "red" else "red"
