import sys
import pygame
from game import Game, State


def draw_pawns():
    for i in range(1, 20):
        if game.board[i] == State.WHITE:
            screen.blit(white, (game.positions[i][0] - 33, game.positions[i][1] - 33))
        elif game.board[i] == State.BLACK:
            screen.blit(black, (game.positions[i][0] - 33, game.positions[i][1] - 33))


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font('assets\Fipps-Regular.otf', 12)

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Lau kata kati')

    background = pygame.image.load('assets/board.png').convert()
    white = pygame.image.load('assets/white.png')
    black = pygame.image.load('assets/black.png')

    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                object_index = game.check_if_clickable(event.pos)
                if object_index is not None:
                    game.add_to_interaction(object_index)

        screen.blit(background, (0, 0))
        draw_pawns()
        if game.white_wins:
            text_surface = font.render('Bialy wygrywa!', False, (0, 0, 0))
        if game.black_wins:
            text_surface = font.render('Czarny wygrywa!', False, (0, 0, 0))
        if game.white_turn and not game.white_wins and not game.black_wins:
            text_surface = font.render('Ruch - bialy', False, (0, 0, 0))
        if not game.white_turn and not game.white_wins and not game.black_wins:
            text_surface = font.render('Ruch - czarny', False, (0, 0, 0))

        screen.blit(text_surface, (10, 10))
        pygame.display.update()
        clock.tick(60)
