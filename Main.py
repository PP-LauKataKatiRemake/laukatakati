import sys
import time
import pygame
from Game_with_computer import GameWithComputer, State


def draw_pawns():
    for i in range(1, 20):
        if game_with_computer.board[i] == State.WHITE:
            screen.blit(white, (game_with_computer.coordinates[i]))
        elif game_with_computer.board[i] == State.BLACK:
            screen.blit(black, (game_with_computer.coordinates[i]))


if __name__ == '__main__':
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont('Arial', 18)
    text_surface = font.render('', False, (0, 0, 0))

    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Lau kata kati')

    background = pygame.image.load('assets/board.png').convert()
    white = pygame.image.load('assets/white.png')
    black = pygame.image.load('assets/black.png')

    clock = pygame.time.Clock()

    game_with_computer = GameWithComputer()
    draw_pawns()

    done = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                object_index = game_with_computer.check_if_clickable(event.pos)
                if object_index is not None:
                    screen.blit(white, (game_with_computer.coordinates[2]))
                    game_with_computer.add_to_interaction(object_index)
                    draw_pawns()
            draw_pawns()

        screen.blit(background, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        time.sleep(0.5)
