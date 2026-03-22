from pygame import Vector2

from Piece import Piece


class Board:
    def __init__(self, grid: list[list[str]]) -> None:
        self._grid: list[list[str]] = grid

    def place_piece(self, piece: Piece):
        form = piece.form.copy()
        for y in range(len(form)):
            for x in range(len(form[y])):
                current_row = y + int(piece.get_position().y)
                current_column = x + int(piece.get_position().x)
                if self._grid[current_row][current_column] != "X":
                    self._grid[current_row][current_column] = form[y][x]

    def freeze_piece(self, piece: Piece):
        form = piece.form.copy()
        for y in range(len(form)):
            for x in range(len(form[y])):
                current_row = y + int(piece.get_position().y)
                current_column = x + int(piece.get_position().x)
                if self._grid[current_row][current_column] == "X":
                    continue
                self._grid[current_row][current_column] = (
                    "X" if form[y][x] == "x" else form[y][x]
                )

    def eliminate_temporary_pieces(self):
        for y in range(len(self._grid)):
            for x in range(len(self._grid[y])):
                if self._grid[y][x] == "x":
                    self._grid[y][x] = "O"

    def clear_completed_rows(self):
        for y in range(len(self._grid) - 1, -1, -1):
            if all([cell == "X" for cell in self._grid[y]]):
                for x in range(len(self._grid[y])):
                    self._grid[y][x] = "O"

    def close_rows_gaps(self):
        most_below_empty_row: int | None = None
        for y in range(len(self._grid) - 1, -1, -1):
            if not any([cell == "X" for cell in self._grid[y]]):
                most_below_empty_row = (
                    y if most_below_empty_row is None else most_below_empty_row
                )
            elif most_below_empty_row:
                for x in range(len(self._grid[y])):
                    self._grid[most_below_empty_row][x] = self._grid[y][x]
                    self._grid[y][x] = "O"
                most_below_empty_row -= 1
