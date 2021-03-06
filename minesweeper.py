import os
import pygame as pg

import random

TILE_WIDTH = 17
TILE_HEIGHT = 17
TILE_DIMENSIONS = (TILE_WIDTH - 1, TILE_HEIGHT - 1)

# SCREEN_WIDTH = 1600
# SCREEN_HEIGHT = 800
SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
SCREEN_DIMENSIONS = (SCREEN_WIDTH, SCREEN_HEIGHT)

NUM_ROWS = SCREEN_HEIGHT // TILE_HEIGHT
print(NUM_ROWS)
NUM_COLS = SCREEN_WIDTH // TILE_WIDTH
print(NUM_COLS)

NUM_TILES = NUM_ROWS * NUM_COLS
print(NUM_TILES)

# NUM_MINES = NUM_TILES // 8
NUM_MINES = 5
print(NUM_MINES)

FONT_SIZE = 21

TILE_NUM_VALUES = [str(x) for x in range(9)]

DIRECTIONS = [
    (-1, -1),  # North West
    (-1, 0),  # North
    (-1, 1),  # North East
    (0, -1),  # West
    (0, 1),  # East
    (1, -1),  # South West
    (1, 0),  # South
    (1, 1)  # South East
]


class Tile():
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.top_draw_pt = row * TILE_HEIGHT
        self.left_draw_pt = col * TILE_WIDTH

        self.label_left_draw_pt = self.left_draw_pt + (TILE_WIDTH // 4)
        self.label_top_draw_pt = self.top_draw_pt + (TILE_HEIGHT // 12)
        self.label_draw_loc = (self.label_left_draw_pt, self.label_top_draw_pt)

        self.is_mine = False
        self.is_flagged = False
        self.proximity = 0
        self.is_revealed = False

        self.label = None

        self.render_rect = pg.Rect((self.left_draw_pt, self.top_draw_pt), TILE_DIMENSIONS)

    def set_flag(self, is_flagged):
        self.is_flagged = is_flagged
        if is_flagged:
            self.label_top_draw_pt = self.top_draw_pt + (TILE_HEIGHT // 32)
            self.label_draw_loc = (self.label_left_draw_pt, self.label_top_draw_pt)
        else:
            self.label_top_draw_pt = self.top_draw_pt + (TILE_HEIGHT // 12)
            self.label_draw_loc = (self.label_left_draw_pt, self.label_top_draw_pt)

    def __str__(self):
        return f'TILE ({self.row}, {self.col}) \n \
               Mine?: {self.is_mine} \n \
               Proximity: {self.proximity} \n \
               Revealed?: {self.is_revealed} \n'


class Minesweeper:
    def __init__(self):
        DEFAULT_FONT = pg.font.SysFont("arial", FONT_SIZE)
        pg.display.set_caption("Minesweeper")

        self.NUMBER_FONT = pg.font.SysFont("arial", 14)
        self.FLAG_FONT = pg.font.SysFont("arial", 18)
        self.MINE_FONT = pg.font.SysFont("arial", 21)

        self.screen = pg.display.set_mode(SCREEN_DIMENSIONS)
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill('black')

        self.board = []
        for i in range(NUM_ROWS):
            tile_row = []
            for j in range(NUM_COLS):
                new_tile = Tile(i, j)
                tile_row.append(new_tile)
            self.board.append(tile_row)

        self.revealed_tiles = set()
        self.tiles_needed = set()
        self.lay_mines()
        self.calculate_mine_proximities()
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                print(self.board[i][j])
        self.draw_tiles()

        self.is_running = True
        self.did_lose = False

    def draw_tiles(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if not self.board[i][j].is_revealed:
                    # Draw Tile
                    pg.draw.rect(self.background, 'gray', self.board[i][j].render_rect)
                else:
                    if self.board[i][j].is_mine:
                        pg.draw.rect(self.background, 'red', self.board[i][j].render_rect)
                    elif self.board[i][j].proximity == 0:
                        pg.draw.rect(self.background, 'black', self.board[i][j].render_rect)

    def draw_labels(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if self.board[i][j].label:
                    if self.board[i][j].is_revealed or self.board[i][j].is_flagged:
                        self.screen.blit(self.board[i][j].label, self.board[i][j].label_draw_loc)


    def show_mines(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                if self.board[i][j].is_mine:
                    self.board[i][j].is_revealed = True

    def lay_mines(self):
        for _ in range(NUM_MINES):
            mine_row = random.randint(0, NUM_ROWS - 1)
            mine_col = random.randint(0, NUM_COLS - 1)
            self.board[mine_row][mine_col].is_mine = True
            self.board[mine_row][mine_col].label = pg.font.Font.render(self.MINE_FONT, '*', False, 'black')

    def calculate_mine_proximities(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].is_mine:
                    for direction in DIRECTIONS:
                        check_row = i + direction[0]
                        check_col = j + direction[1]
                        if self.is_pos_within_board(check_row, check_col, self.board) and \
                                not self.board[check_row][check_col].is_mine:
                            self.board[check_row][check_col].proximity += 1
                            self.board[check_row][check_col].label = \
                                pg.font.Font.render(self.NUMBER_FONT, str(self.board[check_row][check_col].proximity), False, 'blue')
                else:
                    self.tiles_needed.add((i, j))

    def handle_tile_selection(self, row, col):
        if self.board[row][col].proximity == 0:
            selection = self.get_selection_span(row, col)
            for selected_tile in selection:
                self.board[selected_tile[0]][selected_tile[1]].is_revealed = True
                self.revealed_tiles.add((selected_tile[0], selected_tile[1]))
        else:
            self.board[row][col].is_revealed = True
            self.revealed_tiles.add((row, col))

    def get_selection_span(self, row, col):
        frontier = [(row, col)]
        selection_span = [(row, col)]
        seen = set()
        while frontier:
            check_tile = frontier.pop()
            seen.add(check_tile)
            for direction in DIRECTIONS:
                peek_tile_row = check_tile[0] + direction[0]
                peek_tile_col = check_tile[1] + direction[1]
                if self.is_pos_within_board(peek_tile_row, peek_tile_col, self.board) and \
                        (peek_tile_row, peek_tile_col) not in seen:
                    if not self.board[peek_tile_row][peek_tile_col].is_mine and \
                            not self.board[peek_tile_row][peek_tile_col].is_flagged:
                        if self.board[peek_tile_row][peek_tile_col].proximity == 0:
                            frontier.append((peek_tile_row, peek_tile_col))
                        selection_span.append((peek_tile_row, peek_tile_col))
        return selection_span

    def check_for_win(self):
        return len(self.revealed_tiles) == len(self.tiles_needed)

    def is_pos_within_board(self, row, col, board):
        if 0 <= row < len(board) and \
                0 <= col < len(board[0]):
            return True
        return False

    def pos_to_tile_index(self, pos):
        row = pos[1] // TILE_WIDTH
        col = pos[0] // TILE_HEIGHT
        return (row, col)

    def run(self):
        while self.is_running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.is_running = False
                elif event.type == pg.MOUSEBUTTONDOWN and not self.did_lose:
                    selected_row, selected_col = self.pos_to_tile_index(pg.mouse.get_pos())
                    if not self.is_pos_within_board(selected_row, selected_col, self.board):
                        continue
                    selected_tile = self.board[selected_row][selected_col]
                    if not selected_tile.is_revealed:
                        print(selected_tile)
                        if event.button == 1:
                            if selected_tile.is_mine:
                                self.did_lose = True
                                self.show_mines()
                            elif not selected_tile.is_flagged:
                                self.handle_tile_selection(selected_row, selected_col)
                            if self.check_for_win():
                                print('You won!')
                        if event.button == 3:
                            if selected_tile.is_flagged:
                                selected_tile.set_flag(False)
                                selected_tile.label = None
                            else:
                                selected_tile.set_flag(True)
                                selected_tile.label = pg.font.Font.render(self.FLAG_FONT, 'F', False, 'yellow')

            self.draw_tiles()
            self.screen.blit(self.background, (0, 0))
            self.draw_labels()
            pg.display.flip()


def main():
    pg.init()
    pg.font.init()

    minesweeper = Minesweeper()
    minesweeper.run()


if __name__ == "__main__":
    main()
