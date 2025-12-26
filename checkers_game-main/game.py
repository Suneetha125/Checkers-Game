import pygame
from constants import *
from board import Board
from ai import AI
from gui_renderer import GUIRenderer
from utils import opponent

class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board()
        self.turn = "red"
        self.selected = None
        self.ai = AI("black", depth=4)
        self.renderer = GUIRenderer(win)
        self.difficulty = "medium"
        self.levels = {"easy": 2, "medium": 4, "hard": 6}

    def reset(self):
        self.board = Board()
        self.turn = "red"
        self.selected = None

    def update(self):
        self.renderer.draw_board(self.board)

        # highlight selected piece and possible moves
        if self.selected:
            p = self.board.get(self.selected.row, self.selected.col)
            if p:
                self.renderer.highlight_square(p.row, p.col, SELECT, 5)
                for mv in self.board.get_valid_moves(p):
                    self.renderer.highlight_square(mv[0], mv[1], HIGHLIGHT, 4)

        pygame.display.update()

    def select(self, row, col):
        piece = self.board.get(row, col)

        if self.selected:
            sel_piece = self.board.get(self.selected.row, self.selected.col)
            if not sel_piece:
                self.selected = None
                return

            moves = self.board.get_valid_moves(sel_piece)
            for mv in moves:
                r, c, captured = mv
                if (r, c) == (row, col):

                    # animate & move
                    self.renderer.animate_move(sel_piece, r, c, board=self.board)
                    self.board.move(sel_piece, r, c)

                    # capture
                    if captured:
                        for cap in captured:
                            self.board.remove([self.board.get(cap.row, cap.col)])
                        self.renderer.play_capture()
                    else:
                        self.renderer.play_move()

                    pygame.display.update()
                    pygame.time.delay(400)   # HUMAN MOVE DELAY

                    self.selected = None
                    self.change_turn()
                    return

            self.selected = None
            return

        if piece and piece.color == self.turn:
            self.selected = piece

    def change_turn(self):
        self.turn = "black" if self.turn == "red" else "red"

        # AI TURN
        if self.turn == self.ai.color:
            self.ai.depth = self.levels[self.difficulty]
            move = self.ai.pick_move(self.board)

            if move:
                p, (r, c, captured) = move
                piece = self.board.get(p.row, p.col)

                self.renderer.animate_move(piece, r, c, board=self.board)
                self.board.move(piece, r, c)

                if captured:
                    for cap in captured:
                        self.board.remove([self.board.get(cap.row, cap.col)])
                    self.renderer.play_capture()
                else:
                    self.renderer.play_move()

                pygame.display.update()
                pygame.time.delay(600)  # AI DELAY

            self.change_turn()
