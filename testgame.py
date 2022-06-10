import os
import pygame as pg

import pprint
import random

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

NUM_TILES = NUM_ROWS * NUM_COLS
print(NUM_TILES)

NUM_MINES = NUM_TILES // 8
print(NUM_MINES)

FONT_SIZE = 21


def main():
    pg.init()
    pg.font.init()
    default_font = pg.font.SysFont("arial", FONT_SIZE)

    def draw_tiles(show_labels=False):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                # tile_number = (i * NUM_COLS) + j
                possible_nums = [str(x) for x in range(8)]
                tile_label = None
                target_top = (i * TILE_HEIGHT)
                target_left = (j * TILE_WIDTH)
                new_tile = pg.Rect((target_left, target_top), TILE_DIMENSIONS)

                # Draw Tile
                if board_state[i][j] in possible_nums or board_state[i][j] == '*':
                    pg.draw.rect(background, 'gray', new_tile)
                elif board_state[i][j] == 'x':
                    pg.draw.rect(background, 'black', new_tile)

                if show_labels:
                    # Draw Text
                    if board_state[i][j] == '*':
                        tile_label = pg.font.Font.render(default_font, "*", False, 'blue')
                        tile_labels[(target_left + (TILE_WIDTH // 4), target_top + (TILE_HEIGHT // 4))] = tile_label
                    # tile_label = pg.font.Font.render(default_font, board_state[i][j], False, 'blue')
                    # tile_labels[(target_left + (TILE_WIDTH // 4), target_top + (TILE_HEIGHT // 4))] = tile_label

    def set_mines():
        for _ in range(NUM_MINES):
            mine_row = random.randint(0, NUM_ROWS-1)
            mine_col = random.randint(0, NUM_COLS-1)
            board_state[mine_row][mine_col] = '*'

    def calculate_mine_proximities():
        for i in range(len(board_state)):
            for j in range(len(board_state[0])):
                if board_state[i][j] == '*':
                    directions = [
                        (-1, -1), # North West
                        (-1, 0),  # North
                        (-1, 1),  # North East
                        (0, -1),  # West
                        (0, 1),   # East
                        (1, -1),  # South West
                        (1, 0),   # South
                        (1, 1)    # South East
                    ]

                    for direction in directions:
                        check_row = i + direction[0]
                        check_col = j + direction[1]
                        if check_row >= 0 and check_row < len(board_state) and \
                                check_col >= 0 and \
                                check_col < len(board_state[0]) and \
                                board_state[check_row][check_col] != '*':
                            board_state[check_row][check_col] = str(int(board_state[check_row][check_col]) + 1)

    def pos_to_tile_index(pos):
        row = pos[1] // TILE_WIDTH
        col = pos[0] // TILE_HEIGHT
        return (row, col)

    screen = pg.display.set_mode(SCREEN_DIMENSIONS)
    pg.display.set_caption("Minesweeper")

    background = pg.Surface(screen.get_size()).convert()
    background.fill('black')

    tile_labels = {}

    board_state = [['0'] * NUM_COLS for _ in range(NUM_ROWS)]

    set_mines()
    calculate_mine_proximities()
    print(board_state)
    draw_tiles()

    is_running = True
    did_lose = False
    while is_running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_running = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                is_running = False
            elif event.type == pg.MOUSEBUTTONDOWN and not did_lose:
                selected_row, selected_col = pos_to_tile_index(pg.mouse.get_pos())
                selected_tile_marker = board_state[selected_row][selected_col]
                if selected_tile_marker == '*':
                    did_lose = True
                    draw_tiles(True)
                else:
                    board_state[selected_row][selected_col] = 'x'
                    draw_tiles()


        screen.blit(background, (0, 0))

        for tile_loc, tile_label in tile_labels.items():
            screen.blit(tile_label, tile_loc)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
