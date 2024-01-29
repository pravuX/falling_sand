import pygame
from random import choice, random
from pygame.math import clamp

grid_width = 1000
grid_height = 800
# grid_width = 20
# grid_height = 30
grid_dim = 5

grid_cols = grid_width // grid_dim
grid_rows = grid_height // grid_dim
grid = []

empty = pygame.Color(255, 255, 255)
wood = pygame.Color(127, 34, 1)
water = pygame.Color(35, 137, 218)

colors = [
    pygame.Color(246, 215, 176),
    pygame.Color(242, 210, 169),
    pygame.Color(236, 204, 162),
    pygame.Color(231, 196, 150),
    pygame.Color(225, 191, 146)
]


def draw_grid(screen):
    for row in range(grid_rows):
        for col in range(grid_cols):
            color = grid[col][row]
            sqr_x = col * grid_dim
            sqr_y = row * grid_dim
            sqr = pygame.Rect(sqr_x, sqr_y, grid_dim, grid_dim)
            pygame.draw.rect(screen, color, sqr)
            # pygame.draw.rect(screen, "black", sqr, 1)


def brush(keys, m_left, m_right, mouse_x, mouse_y):
    for row in range(grid_rows):
        for col in range(grid_cols):
            sqr_x = col * grid_dim
            sqr_y = row * grid_dim
            if (mouse_x >= sqr_x and mouse_x <= (sqr_x + grid_dim) and
                    mouse_y >= sqr_y and mouse_y <= (sqr_y + grid_dim)):
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        neighbor_col = int(
                            clamp(col + i, 0, grid_cols - 1))
                        neighbor_row = int(
                            clamp(row + j, 0, grid_rows - 1))
                        if grid[neighbor_col][neighbor_row] == empty:
                            new_color = empty
                            if m_left and not keys[pygame.K_e]:
                                new_color = choice(colors)
                                if keys[pygame.K_w]:
                                    new_color = water
                            elif m_right:
                                new_color = wood
                            grid[neighbor_col][neighbor_row] = new_color

                        elif grid[neighbor_col][neighbor_row] == wood:
                            if m_left and keys[pygame.K_e]:
                                grid[neighbor_col][neighbor_row] = empty


def main():

    pygame.init()

    screen = pygame.display.set_mode((grid_width, grid_height))
    clock = pygame.time.Clock()
    running = True
    fps = 1000

    for col in range(grid_cols):
        grid.append(list())
        for row in range(grid_rows):
            grid[col].append(empty)

    while running:
        clock.tick(fps)
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        draw_grid(screen)

        m_left, _, m_right = pygame.mouse.get_pressed()
        brush(keys, m_left, m_right, mouse_x, mouse_y)

        for row in range(grid_rows - 2, -1, -1):
            for col in range(grid_cols - 1, -1, -1):
                color = grid[col][row]

                row_below = clamp(row + 1, 0, grid_rows - 1)
                col_right = int(clamp(col + 1, 0, grid_cols - 1))
                col_left = int(clamp(col - 1, 0, grid_cols - 1))

                color_below = grid[col][row_below]
                color_right = grid[col_right][row]
                color_left = grid[col_left][row]
                color_below_l = grid[col_left][row_below]
                color_below_r = grid[col_right][row_below]

                slide = random()

                if color != empty and color != wood:
                    if color_below == empty:
                        grid[col][row] = empty
                        grid[col][row_below] = color
                    elif slide >= 0.8:
                        if color_below_l == empty and color_below_r == empty:
                            if slide >= 0.4:
                                color_below_l = wood  # not empty
                            else:
                                color_below_r = wood  # not empty

                        if color_below_l == empty:
                            grid[col][row] = empty
                            grid[col_left][row_below] = color

                        elif color_below_r == empty:
                            grid[col][row] = empty
                            grid[col_right][row_below] = color

                        elif color == water:
                            if color_left == empty and color_right == empty:
                                if slide < 0.4:
                                    color_left = wood
                                else:
                                    color_right = wood

                            if color_left == empty:
                                grid[col][row] = empty
                                grid[col_left][row] = color
                            elif color_right == empty:
                                grid[col][row] = empty
                                grid[col_right][row] = color

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
