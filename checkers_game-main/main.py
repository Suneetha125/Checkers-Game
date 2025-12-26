import pygame
from constants import WIDTH, HEIGHT, SQUARE_SIZE, FPS
from game import Game

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    pygame.init()
    pygame.mixer.init()

    win = pygame.display.set_mode((WIDTH + 200, HEIGHT))
    pygame.display.set_caption("Checkers Improved")

    clock = pygame.time.Clock()
    game = Game(win)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] <= WIDTH:
                    r, c = get_row_col_from_mouse(pos)
                    game.select(r, c)

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()
