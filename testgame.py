import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

TILE_WIDTH = 17
TILE_HEIGHT = 17
TILE_DIMENSIONS = (TILE_WIDTH - 1, TILE_HEIGHT - 1)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 800
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

NUM_ROWS = SCREEN_HEIGHT // TILE_HEIGHT
NUM_COLS = SCREEN_WIDTH // TILE_WIDTH


def draw_tiles():
    return


def main():
    pg.init()
    screen = pg.display.set_mode(SCREEN_DIMENSIONS)
    pg.display.set_caption("Test")

    background = pg.Surface(screen.get_size()).convert()
    background.fill('black')

    for i in range(NUM_ROWS):
        for j in range(NUM_COLS):
            target_top = i * TILE_HEIGHT
            target_left = j * TILE_WIDTH
            new_tile = pg.Rect((target_left, target_top), TILE_DIMENSIONS)
            pg.draw.rect(background, 'gray', new_tile)

    is_running = True
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                is_running = False

        screen.blit(background, (0, 0))
        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
