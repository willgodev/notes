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
print(NUM_ROWS)
NUM_COLS = SCREEN_WIDTH // TILE_WIDTH
print(NUM_COLS)

NUM_TILES = NUM_ROWS * NUM_COLS
print(NUM_TILES)

NUM_MINES = NUM_TILES // 8
print(NUM_MINES)

FONT_SIZE = 21

TILE_NUM_VALUES = [str(x) for x in range(9)]

DIRECTIONS = [
    (-1, -1), # North West
    (-1, 0),  # North
    (-1, 1),  # North East
    (0, -1),  # West
    (0, 1),   # East
    (1, -1),  # South West
    (1, 0),   # South
    (1, 1)    # South East
]

def main():
    pg.init()
    pg.font.init()
    default_font = pg.font.SysFont("arial", FONT_SIZE)

    tile_labels = {}
    flags = {}

    board_state = [['0'] * NUM_COLS for _ in range(NUM_ROWS)]

    screen = pg.display.set_mode(SCREEN_DIMENSIONS)
    pg.display.set_caption("Minesweeper")

    background = pg.Surface(screen.get_size()).convert()
    background.fill('black')

    def draw_tiles(show_labels=False):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                # tile_number = (i * NUM_COLS) + j
                tile_label = None
                target_top = (i * TILE_HEIGHT)
                target_left = (j * TILE_WIDTH)
                new_tile = pg.Rect((target_left, target_top), TILE_DIMENSIONS)

                # Draw Tile
                if board_state[i][j] in TILE_NUM_VALUES or board_state[i][j] == '*':
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

                    for direction in DIRECTIONS:
                        check_row = i + direction[0]
                        check_col = j + direction[1]
                        if check_row >= 0 and check_row < len(board_state) and \
                                check_col >= 0 and \
                                check_col < len(board_state[0]) and \
                                board_state[check_row][check_col] != '*':
                            board_state[check_row][check_col] = str(int(board_state[check_row][check_col]) + 1)

    def handle_tile_selection(row, col):
        selected_tile_marker = board_state[row][col]
        target_top = (row * TILE_HEIGHT)
        target_left = (col * TILE_WIDTH)
        new_tile = pg.Rect((target_left, target_top), TILE_DIMENSIONS)
        number_font = pg.font.SysFont("arial", 14)
        selection = [(row, col)]
        if selected_tile_marker == '0':
            board_state[row][col] = 'x'
            selection += get_selection_span(row, col)
            for selected_tile in selection:
                selected_tile_marker = board_state[selected_tile[0]][selected_tile[1]]
                if selected_tile_marker in TILE_NUM_VALUES:
                    target_top = (selected_tile[0] * TILE_HEIGHT)
                    target_left = (selected_tile[1] * TILE_WIDTH)
                    if selected_tile_marker == '0':
                        pg.draw.rect(background, 'black', new_tile)
                    else:
                        tile_label = pg.font.Font.render(number_font, selected_tile_marker, False, 'blue')
                        tile_labels[(target_left + (TILE_WIDTH // 4), target_top + (TILE_HEIGHT // 8))] = tile_label
        else:
            pg.draw.rect(background, 'black', new_tile)
            if selected_tile_marker != 'x':
                tile_label = pg.font.Font.render(number_font, selected_tile_marker, False, 'blue')
                tile_labels[(target_left + (TILE_WIDTH // 4), target_top + (TILE_HEIGHT // 8))] = tile_label

    def get_selection_span(row, col):
        frontier = [(row, col)]
        selection_span = [(row, col)]
        while frontier:
            check_tile = frontier.pop()
            frontier_tile_row = check_tile[0]
            frontier_tile_col = check_tile[1]
            for direction in DIRECTIONS:
                peek_tile_row = frontier_tile_row + direction[0]
                peek_tile_col = frontier_tile_col + direction[1]
                if peek_tile_row >= 0 and peek_tile_row < len(board_state) and \
                        peek_tile_col >= 0 and peek_tile_col < len(board_state[0]):
                    if board_state[peek_tile_row][peek_tile_col] in TILE_NUM_VALUES:
                        selection_span.append((peek_tile_row, peek_tile_col))
                    if board_state[peek_tile_row][peek_tile_col] == '0':
                        board_state[peek_tile_row][peek_tile_col] = 'x'
                        frontier.append((peek_tile_row, peek_tile_col))
        return selection_span

    def handle_flag_selection(row, col):
        if board_state[row][col] == '0':
            target_top = (row * TILE_HEIGHT)
            target_left = (col * TILE_WIDTH)
            number_font = pg.font.SysFont("arial", 14)
            tile_label = pg.font.Font.render(number_font, '!', False, 'blue')
            tile_labels[(target_left + (TILE_WIDTH // 4), target_top + (TILE_HEIGHT // 8))] = tile_label

    def pos_to_tile_index(pos):
        row = pos[1] // TILE_WIDTH
        col = pos[0] // TILE_HEIGHT
        return (row, col)

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
                if event.button == 1:
                    if selected_tile_marker == '*':
                        did_lose = True
                        draw_tiles(True)
                    else:
                        handle_tile_selection(selected_row, selected_col)
                        draw_tiles()
                if event.button == 3:
                    print('right click')
                    handle_flag_selection(selected_row, selected_col)

        screen.blit(background, (0, 0))

        for tile_loc, tile_label in tile_labels.items():
            screen.blit(tile_label, tile_loc)
        for flag_loc, flag_label in flags:
            screen.blit(flag_label, flag_loc)

        pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    main()
