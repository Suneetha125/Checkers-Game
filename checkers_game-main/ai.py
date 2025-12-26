from board import Board
from constants import MAN_VAL, KING_VAL, ROWS
from utils import opponent
import math
import random


class AI:
    def __init__(self, color="black", depth=4):
        self.color = color
        self.depth = depth

    # ---------------------------------------------------------
    #  EVALUATION FUNCTION  — scores how good a board is
    # ---------------------------------------------------------
    def evaluate(self, board):
        my_pieces = board.get_all_pieces(self.color)
        opp_pieces = board.get_all_pieces(opponent(self.color))

        score = 0

        # Material score (kings are more valuable)
        for p in my_pieces:
            score += KING_VAL if p.king else MAN_VAL
        for p in opp_pieces:
            score -= KING_VAL if p.king else MAN_VAL

        # Mobility score (having more legal moves is good)
        score += 5 * (
            sum(len(board.get_valid_moves(p)) for p in my_pieces)
            - sum(len(board.get_valid_moves(p)) for p in opp_pieces)
        )

        # Center control (pieces near center are stronger)
        for p in my_pieces:
            if 2 <= p.row <= 5 and 2 <= p.col <= 5:
                score += 3
        for p in opp_pieces:
            if 2 <= p.row <= 5 and 2 <= p.col <= 5:
                score -= 3

        return score

    # ---------------------------------------------------------
    #  PICK BEST MOVE USING MINIMAX
    # ---------------------------------------------------------
    def pick_move(self, board):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf

        pieces = board.get_all_pieces(self.color)
        all_moves = []

        # Collect all moves
        for p in pieces:
            for mv in board.get_valid_moves(p):
                all_moves.append((p, mv))

        # Shuffle to avoid deterministic patterns
        random.shuffle(all_moves)

        # Evaluate each move using minimax
        for p, mv in all_moves:
            bcopy = board.copy()
            pcopy = bcopy.get(p.row, p.col)
            r, c, captured = mv

            # Apply move on hypothetical board
            bcopy.move(pcopy, r, c)
            for cap in captured:
                bcopy.remove([bcopy.get(cap.row, cap.col)])

            # Minimax step
            val = self._minimax(bcopy, self.depth - 1, alpha, beta, False)

            # Best move update
            if val > best_score:
                best_score = val
                best_move = (p, mv)

            alpha = max(alpha, best_score)

        return best_move

    # ---------------------------------------------------------
    #  MINIMAX + ALPHA BETA
    # ---------------------------------------------------------
    def _minimax(self, board, depth, alpha, beta, maximizing):
        # Check terminal states
        result = board.winner()

        if depth == 0 or result:
            if result == self.color:
                return 100000
            if result == opponent(self.color):
                return -100000
            return self.evaluate(board)

        # ----------------------------------
        #  MAXIMIZING PLAYER (AI)
        # ----------------------------------
        if maximizing:
            max_val = -math.inf
            for p in board.get_all_pieces(self.color):
                for mv in board.get_valid_moves(p):
                    bcopy = board.copy()
                    pcopy = bcopy.get(p.row, p.col)
                    r, c, captured = mv

                    bcopy.move(pcopy, r, c)
                    for cap in captured:
                        bcopy.remove([bcopy.get(cap.row, cap.col)])

                    val = self._minimax(bcopy, depth - 1, alpha, beta, False)
                    max_val = max(max_val, val)
                    alpha = max(alpha, val)

                    if beta <= alpha:
                        return max_val

            return max_val

        # ----------------------------------
        #  MINIMIZING PLAYER (Human)
        # ----------------------------------
        else:
            min_val = math.inf
            opp = opponent(self.color)

            for p in board.get_all_pieces(opp):
                for mv in board.get_valid_moves(p):
                    bcopy = board.copy()
                    pcopy = bcopy.get(p.row, p.col)
                    r, c, captured = mv

                    bcopy.move(pcopy, r, c)
                    for cap in captured:
                        bcopy.remove([bcopy.get(cap.row, cap.col)])

                    val = self._minimax(bcopy, depth - 1, alpha, beta, True)

                    min_val = min(min_val, val)
                    beta = min(beta, val)

                    if beta <= alpha:
                        return min_val

            return min_val
