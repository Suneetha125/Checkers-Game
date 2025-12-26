from dataclasses import dataclass

@dataclass
class Piece:
    row: int
    col: int
    color: str
    king: bool = False

    def make_king(self):
        self.king = True

    def copy(self):
        return Piece(self.row, self.col, self.color, self.king)
