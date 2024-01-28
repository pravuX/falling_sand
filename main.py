import pygame
from random import randint, choice
from pygame.math import clamp


class Cell():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        # colors other than empty indicate the presence on sand on the grid
        self.color = color
        self.velocity = 1

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def get_pos(self):
        return self.x, self.y

    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_velocity(self, velocity):
        self.velocity = velocity

    def get_velocity(self):
        return self.velocity


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
    grid_width = 800
    grid_height = 800
    grid_dim = 100
    grid_size = grid_width // grid_dim

    pygame.init()

    screen = pygame.display.set_mode((grid_width, grid_height))
    clock = pygame.time.Clock()
    running = True
    fps = 60
    empty = pygame.Color(255, 255, 255)
    wood = pygame.Color(127, 34, 1)

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

        for col in range(0, grid_dim):
            for row in range(0, grid_dim):
                cell = grid[row + col * grid_dim]
                rect_x = col * grid_size
                rect_y = row * grid_size
                rect = pygame.Rect(rect_x, rect_y, grid_size, grid_size)
                pygame.draw.rect(screen, cell.get_color(), rect)
                # pygame.draw.rect(screen, "black", rect, 1)

        m_left, _, m_right = pygame.mouse.get_pressed()
        if m_left:
            for cell_idx in range(0, len(grid)):
                cell = grid[cell_idx]
                cell_x, cell_y = cell.get_pos()
                cell_x *= grid_size
                cell_y *= grid_size
                cell_color = cell.get_color()
                if (mouse_x >= cell_x and mouse_x <= (cell_x + grid_size) and
                        mouse_y >= cell_y and mouse_y <= (cell_y + grid_size)):
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            neighbor_x = clamp(
                                cell_x // grid_size + i, 0, grid_dim-1)
                            neighbor_y = clamp(
                                cell_y // grid_size + j, 0, grid_dim-1)

                            neighbor_idx = int(
                                neighbor_y + neighbor_x * grid_dim)
                            if grid[neighbor_idx].get_color() == empty:
                                new_color = choice(colors)
                                grid[neighbor_idx].set_color(
                                    pygame.Color(*new_color))

                    # new_color = hsv_to_rgb((color % 360) / 360.0, 0.285, 0.965, 1.0)
                    # color += 1

        elif m_right:
            for cell_idx in range(0, len(grid)):
                cell = grid[cell_idx]
                cell_x, cell_y = cell.get_pos()
                cell_x *= grid_size
                cell_y *= grid_size
                cell_color = cell.get_color()
                if (mouse_x >= cell_x and mouse_x <= (cell_x + grid_size) and
                        mouse_y >= cell_y and mouse_y <= (cell_y + grid_size)):
                    if cell_color == empty and not keys[pygame.K_e]:
                        grid[cell_idx].set_color(pygame.Color(wood))
                    elif keys[pygame.K_e]:
                        grid[cell_idx].set_color(pygame.Color(empty))

        # for col in range(grid_dim - 1, -1, -1):
        for col in range(0, grid_dim):
            for row in range(grid_dim - 2, -1, -1):
                cell_idx = row + col * grid_dim
                cell_color = grid[cell_idx].get_color()

                if cell_color != empty and cell_color != wood:
                    row_below = int(clamp(row + 1, 0, grid_dim - 1))
                    cell_below_idx = row_below + col * grid_dim

                    col_right = int(clamp(col + 1, 0, grid_dim - 1))
                    cell_below_right_idx = row_below + col_right * grid_dim

                    col_left = int(clamp(col - 1, 0, grid_dim - 1))
                    cell_below_left_idx = row_below + col_left * grid_dim

                    slide = randint(0, 1)

                    if grid[cell_below_idx].get_color() == empty and grid[cell_below_idx].get_color() != wood:
                        grid[cell_below_idx].set_color(cell_color)
                        grid[cell_idx].set_color(empty)

                    elif slide == 1 and grid[cell_below_idx].get_color() != wood:
                        if grid[cell_below_left_idx].get_color() == empty:
                            grid[cell_below_left_idx].set_color(cell_color)
                            grid[cell_idx].set_color(empty)

                        elif grid[cell_below_right_idx].get_color() == empty:
                            grid[cell_below_right_idx].set_color(cell_color)
                            grid[cell_idx].set_color(empty)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
