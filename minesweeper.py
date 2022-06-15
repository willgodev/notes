import os
import pygame as pg

import random

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
    (-1, -1),  # North West
    (-1, 0),   # North
    (-1, 1),   # North East
    (0, -1),   # West
    (0, 1),    # East
    (1, -1),   # South West
    (1, 0),    # South
    (1, 1)     # South East
]

class Tile():
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.top_draw_pt = row * TILE_HEIGHT
        self.left_draw_pt = col * TILE_WIDTH

        self.is_mine = False
        self.proximity = 0
        self.isRevealed = False

        self.label = None

        self.render_rect = pg.Rect((self.left_draw_pt, self.top_draw_pt), TILE_DIMENSIONS)

class Minesweeper:
    def __init__(self):
        DEFAULT_FONT = pg.font.SysFont("arial", FONT_SIZE)
        pg.display.set_caption("Minesweeper")

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

        self.draw_tiles()

        self.is_running = True
        self.did_lose = False

    def draw_tiles(self):
        for i in range(NUM_ROWS):
            for j in range(NUM_COLS):
                # Draw Tile
                pg.draw.rect(self.background, 'gray', self.board[i][j].render_rect)

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
                    self.draw_tiles()

            self.screen.blit(self.background, (0, 0))
            pg.display.flip()

def main():
    pg.init()
    pg.font.init()

    minesweeper = Minesweeper()
    minesweeper.run()

if __name__ == "__main__":
    main()