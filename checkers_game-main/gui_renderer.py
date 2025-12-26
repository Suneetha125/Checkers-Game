import pygame
import os
from constants import *
from typing import Optional

class GUIRenderer:
    def __init__(self, win: pygame.Surface, assets_available=True, enable_sounds=True):
        self.win = win
        self.assets_available = assets_available
        self.enable_sounds = enable_sounds
        self._load_assets()

    def _load_assets(self):
        try:
            if os.path.exists(BOARD_IMAGE):
                self.board_img = pygame.transform.scale(
                    pygame.image.load(BOARD_IMAGE).convert_alpha(),
                    (WIDTH, HEIGHT)
                )
            else:
                self.board_img = None

            if os.path.exists(PIECE_RED_IMG):
                img = pygame.image.load(PIECE_RED_IMG).convert_alpha()
                self.piece_red = pygame.transform.smoothscale(img, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
            else:
                self.piece_red = None

            if os.path.exists(PIECE_BLACK_IMG):
                img = pygame.image.load(PIECE_BLACK_IMG).convert_alpha()
                self.piece_black = pygame.transform.smoothscale(img, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
            else:
                self.piece_black = None

            if os.path.exists(CROWN_IMG):
                crown = pygame.image.load(CROWN_IMG).convert_alpha()
                self.crown = pygame.transform.smoothscale(crown, (SQUARE_SIZE // 2, SQUARE_SIZE // 2))
            else:
                self.crown = None

        except:
            self.board_img = self.piece_red = self.piece_black = self.crown = None

        if self.enable_sounds:
            try:
                self.click_sound = pygame.mixer.Sound(CLICK_SOUND) if os.path.exists(CLICK_SOUND) else None
                self.move_sound = pygame.mixer.Sound(MOVE_SOUND) if os.path.exists(MOVE_SOUND) else None
                self.capture_sound = pygame.mixer.Sound(CAPTURE_SOUND) if os.path.exists(CAPTURE_SOUND) else None
            except:
                self.click_sound = self.move_sound = self.capture_sound = None
        else:
            self.click_sound = self.move_sound = self.capture_sound = None

    # ----- Sounds -----
    def play_click(self):
        if self.click_sound:
            self.click_sound.play()

    def play_move(self):
        if self.move_sound:
            self.move_sound.play()

    def play_capture(self):
        if self.capture_sound:
            self.capture_sound.play()

    # ----- Main board drawing -----
    def draw_board(self, board):
        # Background
        if self.board_img:
            self.win.blit(self.board_img, (0, 0))
        else:
            self.win.fill(BLACK)
            for r in range(ROWS):
                for c in range(COLS):
                    color = WHITE if (r + c) % 2 == 0 else GREY
                    pygame.draw.rect(self.win, color, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Draw pieces
        for r in range(ROWS):
            for c in range(COLS):
                p = board.get(r, c)
                if p:
                    x = c * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = r * SQUARE_SIZE + SQUARE_SIZE // 2

                    if p.color == "red":
                        if self.piece_red:
                            self.win.blit(self.piece_red, self.piece_red.get_rect(center=(x, y)))
                        else:
                            pygame.draw.circle(self.win, RED, (x, y), SQUARE_SIZE // 2 - 12)
                    else:
                        if self.piece_black:
                            self.win.blit(self.piece_black, self.piece_black.get_rect(center=(x, y)))
                        else:
                            pygame.draw.circle(self.win, GREEN, (x, y), SQUARE_SIZE // 2 - 12)

                    if p.king:
                        if self.crown:
                            self.win.blit(self.crown, self.crown.get_rect(center=(x, y - 5)))
                        else:
                            pygame.draw.circle(self.win, BLACK, (x, y - 5), 7)

        # Score panel on the right
        self.draw_score_panel(board)

    # ----- Score Panel -----
    def draw_score_panel(self, board):
        panel_x = WIDTH
        pygame.draw.rect(self.win, (40, 40, 40), (panel_x, 0, 200, HEIGHT))

        font = pygame.font.SysFont("arial", 24)
        big = pygame.font.SysFont("arial", 28, bold=True)

        title = big.render("SCORE", True, (255, 255, 255))
        self.win.blit(title, (panel_x + 50, 20))

        red = len(board.get_all_pieces("red"))
        black = len(board.get_all_pieces("black"))

        rtxt = font.render(f"Red: {red}", True, (220, 70, 70))
        btxt = font.render(f"Black: {black}", True, (70, 200, 70))

        self.win.blit(rtxt, (panel_x + 20, 80))
        self.win.blit(btxt, (panel_x + 20, 120))

    # ----- Highlight -----
    def highlight_square(self, row, col, color=HIGHLIGHT, width=4):
        pygame.draw.rect(self.win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), width)

    # ----- Fixed Smooth Animation (no ghost piece) -----
    def animate_move(self, piece, r, c, board):
        # Remove piece from old square while animating
        original_row, original_col = piece.row, piece.col
        board.board[original_row][original_col] = None

        sx = original_col * SQUARE_SIZE + SQUARE_SIZE // 2
        sy = original_row * SQUARE_SIZE + SQUARE_SIZE // 2
        ex = c * SQUARE_SIZE + SQUARE_SIZE // 2
        ey = r * SQUARE_SIZE + SQUARE_SIZE // 2

        steps = 18
        clock = pygame.time.Clock()

        for i in range(1, steps + 1):
            t = i / steps
            x = int(sx + (ex - sx) * t)
            y = int(sy + (ey - sy) * t)

            self.draw_board(board)

            # Draw moving piece manually
            color = RED if piece.color == "red" else GREEN
            pygame.draw.circle(self.win, color, (x, y), SQUARE_SIZE // 2 - 12)

            if piece.king and self.crown:
                self.win.blit(self.crown, self.crown.get_rect(center=(x, y - 5)))

            pygame.display.update()
            clock.tick(30)

        # Restore piece in final spot
        piece.row, piece.col = r, c
        board.board[r][c] = piece
