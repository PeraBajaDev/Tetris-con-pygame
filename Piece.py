import pygame

from pieces_form import pieces_form


class Piece:
    def __init__(
        self, position: pygame.Vector2, form_letter: str, grid_size: pygame.Vector2
    ):
        self._position: pygame.Vector2 = position
        self.form: list[list[str]] = pieces_form[form_letter].copy()
        self.grid_size: pygame.Vector2 = grid_size

    def get_position(self):
        return self._position

    def set_position(self, value: pygame.Vector2):
        self._position = value

    def move(self, direction: pygame.Vector2, grid: list[list[str]]):
        new_position = direction + self._position
        new_position.x = pygame.math.clamp(
            new_position.x, 0, self.grid_size.x - len(self.form[0])
        )
        new_position.y = pygame.math.clamp(
            new_position.y, 0, self.grid_size.y - len(self.form)
        )
        if self.is_next_position_occupied(grid, new_position):
            return
        self._position = new_position

    def is_next_position_occupied(
        self,
        grid: list[list[str]],
        next_position: pygame.Vector2,
        form: list[list[str]] | None = None,
    ):
        form = self.form if form is None else form
        try:
            for y in range(len(form)):
                for x in range(len(form[y])):
                    if form[y][x] == "O":
                        continue
                    if grid[y + int(next_position.y)][x + int(next_position.x)] == "X":
                        return True
        except IndexError:
            return True

        return False

    def rotate(self, grid) -> None:
        rotated_form: list[list[str]] = [[] for _ in range(len(self.form[0]))]
        for x in range(len(self.form[0]) - 1, -1, -1):
            for y in range(len(self.form) - 1, -1, -1):
                rotated_form[x].append(self.form[y][x])
        if self.is_next_position_occupied(grid, self._position, rotated_form):
            return
        self.form = rotated_form
