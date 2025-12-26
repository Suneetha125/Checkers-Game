from piece import Piece
from constants import ROWS, COLS, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT
from utils import in_bounds

class Board:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self._setup()

    def _setup(self):
        for r in range(ROWS):
            for c in range(COLS):
                if (r + c) % 2 == 1:
                    if r < 3:
                        self.board[r][c] = Piece(r, c, "black")
                    elif r > 4:
                        self.board[r][c] = Piece(r, c, "red")

    def get(self, r, c):
        return self.board[r][c]

    def move(self, piece, r, c):
        self.board[piece.row][piece.col] = None
        piece.row, piece.col = r, c
        self.board[r][c] = piece

        if piece.color == "red" and r == 0:
            piece.make_king()
        elif piece.color == "black" and r == ROWS - 1:
            piece.make_king()

    def remove(self, pieces):
        for p in pieces:
            if p:
                self.board[p.row][p.col] = None

    def copy(self):
        new_board = Board.__new__(Board)
        new_board.board = [[None for _ in range(COLS)] for _ in range(ROWS)]

        for r in range(ROWS):
            for c in range(COLS):
                p = self.board[r][c]
                if p:
                    new_board.board[r][c] = p.copy()

        return new_board

    def get_all_pieces(self, color):
        return [self.board[r][c]
                for r in range(ROWS)
                for c in range(COLS)
                if self.board[r][c] and self.board[r][c].color == color]

    def get_valid_moves(self, piece):
        moves = []
        directions = []

        if piece.king:
            directions = [UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]
        else:
            directions = [UP_LEFT, UP_RIGHT] if piece.color == "red" else [DOWN_LEFT, DOWN_RIGHT]

        for d in directions:
            r1 = piece.row + d[0]
            c1 = piece.col + d[1]
            if in_bounds(r1, c1) and self.get(r1, c1) is None:
                moves.append((r1, c1, []))

        for d in directions:
            r1 = piece.row + d[0]
            c1 = piece.col + d[1]
            r2 = piece.row + 2 * d[0]
            c2 = piece.col + 2 * d[1]

            if in_bounds(r2, c2):
                mid = self.get(r1, c1)
                end = self.get(r2, c2)
                if mid and mid.color != piece.color and end is None:
                    moves.append((r2, c2, [mid]))

        return moves

    def winner(self):
        reds = self.get_all_pieces("red")
        blacks = self.get_all_pieces("black")

        if not reds:
            return "black"
        if not blacks:
            return "red"

        return None
