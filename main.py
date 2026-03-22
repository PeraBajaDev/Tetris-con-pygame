import random

import pygame
from pygame import Vector2

from Board import Board
from Piece import Piece
from pieces_form import pieces_form

WIDTH: int = 16 * 60
HEIGHT: int = 9 * 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()
clock = pygame.time.Clock()
ball_position = Vector2(WIDTH // 2, HEIGHT // 2)
grid = [["X" for _ in range(10)] for _ in range(20)]
board = Board(grid)
CELL_SIZE = 25
speed: float = 200
piece_O: Piece = Piece(Vector2(0, 0), "O", pygame.Vector2(len(grid[0]), len(grid)))
freezing_timer: float = 0.7
falling_force = Vector2(0, 0)
piece_falling_event = pygame.USEREVENT
pygame.time.set_timer(piece_falling_event, 1000)
text = pygame.font.SysFont(pygame.font.get_default_font(), 14, bold=True)


def get_move_direction_from_input(key) -> Vector2:
    move_direction = Vector2(0, 0)
    if key == pygame.K_w:
        piece_O.rotate(grid)
    if key == pygame.K_s:
        move_direction.y = 1

    if key == pygame.K_a:
        move_direction.x = -1
    elif key == pygame.K_d:
        move_direction.x = 1
    return move_direction


def draw_grid():
    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            lines = [
                Vector2(x * CELL_SIZE, y * CELL_SIZE),
                Vector2(x * CELL_SIZE, y * CELL_SIZE + CELL_SIZE),
                Vector2(x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE),
                Vector2(x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE),
            ]
            pygame.draw.lines(
                screen,
                "white",
                True,
                lines,
            )
            cell_color: str = ""
            match grid[y][x]:
                case "x":
                    cell_color = "green"
                case "O":
                    cell_color = "black"
                case "X":
                    cell_color = "white"

            pygame.draw.rect(
                screen,
                cell_color,
                pygame.Rect(
                    x * CELL_SIZE + 1, y * CELL_SIZE + 1, CELL_SIZE - 1, CELL_SIZE - 1
                ),
            )


move_direction = Vector2(0, 0)

while True:
    move_direction *= 0
    falling_force = Vector2(0, 0)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            move_direction = get_move_direction_from_input(event.key)
        if event.type == piece_falling_event:
            falling_force = Vector2(0, 1)
    delta: float = clock.tick(60) / 1000

    screen.fill("black")
    board.place_piece(piece_O)
    if piece_O.is_next_position_occupied(grid, piece_O.get_position() + Vector2(0, 1)):
        if freezing_timer <= 0:
            board.freeze_piece(piece_O)
            freezing_timer = 0.7
        else:
            freezing_timer -= delta
    draw_grid()
    if all([not any([cell == "x" for cell in row]) for row in grid]):
        piece_O.set_position(Vector2(4, 0))
        piece_O.form = random.choice(list(pieces_form.values()))
    board.eliminate_temporary_pieces()
    board.clear_completed_rows()
    board.close_rows_gaps()
    piece_O.move(move_direction + falling_force, grid)
    text_surface = text.render(
        f"piece_position: {piece_O.get_position()}", True, "white"
    )
    screen.blit(text_surface, (700, 200))
    pygame.display.flip()
