import pygame
from random import random, choice
from pygame.math import clamp


class Cell():
    def __init__(self, x, y, color):
        self.x = x  # col
        self.y = y  # row
        # this serves as the type of the cell
        # empty cells have white color
        # sand particles have one of the colors from the colors array
        # wood particles have "wood" color
        # water particles have "water" color
        self.color = color

    def get_pos(self):
        return self.x, self.y


def hsv_to_rgb(h, s, v, a):
    a = int(255*a)
    if s:
        if h == 1.0:
            h = 0.0
        i = int(h*6.0)
        f = h*6.0 - i

        w = int(255*(v * (1.0 - s)))
        q = int(255*(v * (1.0 - s * f)))
        t = int(255*(v * (1.0 - s * (1.0 - f))))
        v = int(255*v)

        if i == 0:
            return (v, t, w, a)
        if i == 1:
            return (q, v, w, a)
        if i == 2:
            return (w, v, t, a)
        if i == 3:
            return (w, q, v, a)
        if i == 4:
            return (t, w, v, a)
        if i == 5:
            return (v, w, q, a)
    else:
        v = int(255*v)
        return (v, v, v, a)


def main():
    grid_width = 512
    grid_height = 512
    grid_dim = 128
    grid_size = grid_width // grid_dim

    pygame.init()

    screen = pygame.display.set_mode((grid_width, grid_height))
    clock = pygame.time.Clock()
    running = True
    fps = 1000
    empty = pygame.Color(255, 255, 255)
    wood = pygame.Color(127, 34, 1)
    water = pygame.Color(35, 137, 218)
    gravity = 1

    grid = []
    colors = [
        pygame.Color(246, 215, 176),
        pygame.Color(242, 210, 169),
        pygame.Color(236, 204, 162),
        pygame.Color(231, 196, 150),
        pygame.Color(225, 191, 146)
    ]
    # color = 0

    for col in range(0, grid_dim):
        for row in range(0, grid_dim):
            grid.append(Cell(col, row, empty))

    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        m_left, _, m_right = pygame.mouse.get_pressed()
        for cell_idx in range(0, len(grid)):
            cell = grid[cell_idx]
            cell_col, cell_row = cell.get_pos()

            cell_col_scaled = cell_col * grid_size
            cell_row_scaled = cell_row * grid_size
            cell_color = cell.color

            rect = pygame.Rect(
                cell_col_scaled, cell_row_scaled, grid_size, grid_size)
            pygame.draw.rect(screen, cell.color, rect)
            # pygame.draw.rect(screen, "black", rect, 1)

            if (mouse_x >= cell_col_scaled and mouse_x <= (cell_col_scaled + grid_size) and
                    mouse_y >= cell_row_scaled and mouse_y <= (cell_row_scaled + grid_size)):
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        neighbor_col = clamp(cell_col + i, 0, grid_dim-1)
                        neighbor_row = clamp(cell_row + j, 0, grid_dim-1)

                        neighbor_idx = int(
                            neighbor_col * grid_dim + neighbor_row)

                        if grid[neighbor_idx].color == empty:
                            new_color = empty
                            if m_left and not keys[pygame.K_e]:
                                new_color = choice(colors)
                                if keys[pygame.K_w]:
                                    new_color = water
                            elif m_right:
                                new_color = pygame.Color(wood)

                            grid[neighbor_idx].color = pygame.Color(
                                *new_color)
                            grid[neighbor_idx].velocity = 1

                        elif grid[neighbor_idx].color == wood:
                            if m_left and keys[pygame.K_e]:
                                grid[neighbor_idx].color = empty
                                grid[neighbor_idx].velocity = 0

        for col in range(0, grid_dim):
            for row in range(grid_dim - 2, -1, -1):
                cell_idx = row + col * grid_dim
                cell_color = grid[cell_idx].color

                if cell_color != empty and cell_color != wood:
                    row_below = int(
                        clamp(row + 1, 0, grid_dim - 1))
                    cell_below_idx = row_below + col * grid_dim

                    col_right = int(
                        clamp(col + 1, 0, grid_dim - 1))
                    col_left = int(clamp(col - 1, 0, grid_dim - 1))
                    cell_right_idx = row + col_right * grid_dim
                    cell_left_idx = row + col_left * grid_dim
                    cell_below_right_idx = row_below + col_right * grid_dim
                    cell_below_left_idx = row_below + col_left * grid_dim

                    below_is_empty = grid[cell_below_idx].color == empty
                    below_right_is_empty = grid[cell_below_right_idx].color == empty
                    below_left_is_empty = grid[cell_below_left_idx].color == empty
                    right_is_empty = grid[cell_right_idx].color == empty
                    left_is_empty = grid[cell_left_idx].color == empty

                    slide = random()

                    # if grid[cell_below_idx].color == empty:
                    if below_is_empty:
                        grid[cell_below_idx].color = cell_color
                        grid[cell_idx].color = empty

                    elif slide > 0.8:

                        # if (below_left_is_empty and below_right_is_empty):
                        #     if slide < 0.5:
                        #         below_left_is_empty = False
                        #     else:
                        #         below_right_is_empty = False

                        if below_left_is_empty:
                            grid[cell_below_left_idx].color = cell_color
                            grid[cell_idx].color = empty

                        elif below_right_is_empty:
                            grid[cell_below_right_idx].color = cell_color
                            grid[cell_idx].color = empty

                        elif cell_color == water:

                            if (left_is_empty and right_is_empty):
                                if slide < 0.4:
                                    left_is_empty = False
                                else:
                                    right_is_empty = False

                            if left_is_empty:
                                grid[cell_left_idx].color = cell_color
                                grid[cell_idx].color = empty

                            elif right_is_empty:
                                grid[cell_right_idx].color = cell_color
                                grid[cell_idx].color = empty

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
