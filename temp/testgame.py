import os
import pygame as pg

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

def draw_tiles():
    return

def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Test")

    background = pg.Surface(screen.get_size()).convert()
    background.fill('black')

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
