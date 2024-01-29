import pygame


def main():
    grid_width = 400
    grid_height = 200
    pygame.init()

    surface = pygame.display.set_mode((grid_width, grid_height))

    px_array = pygame.PixelArray(surface)
    clock = pygame.time.Clock()
    fps = 120
    running = True
    black = pygame.Color(0, 0, 0)
    color = 0

    while running:
        clock.tick(fps)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        m_left, _, _ = pygame.mouse.get_pressed()
        if m_left:
            px_color = surface.get_at((mouse_x, mouse_y))
            n_h, n_s, n_v, n_a = px_color.hsva
            n_h = color % 360
            n_s = 28.5
            n_v = 96.5
            px_color.hsva = n_h, n_s, n_v, n_a
            px_array[mouse_x, mouse_y] = surface.map_rgb(px_color)

            color += 1

        # iterate in reverse order to prevent updating previously
        # updated pixel
        for row in range(grid_height - 2, -1, -1):
            for col in range(grid_width - 1, -1, -1):
                # having non black color is having sand on the pixel
                if px_array[col, row] != surface.map_rgb(black):
                    row_below = int(pygame.math.clamp(
                        row + 1, 0, grid_height - 1))
                    col_right = int(pygame.math.clamp(
                        col + 1, 0, grid_width - 1))
                    col_left = int(pygame.math.clamp(
                        col - 1, 0, grid_width - 1))
                    if px_array[col, row_below] == surface.map_rgb(black):
                        px_array[col, row_below] = px_array[col, row]
                        px_array[col, row] = pygame.Color(black)
                    elif px_array[col_right, row_below] == surface.map_rgb(black):
                        px_array[col_right, row_below] = px_array[col, row]
                        px_array[col, row] = pygame.Color(black)
                    elif px_array[col_left, row_below] == surface.map_rgb(black):
                        px_array[col_left, row_below] = px_array[col, row]
                        px_array[col, row] = pygame.Color(black)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
