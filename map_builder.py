from typing import Tuple

import pygame as pg

from domain.entities import Cell
from domain.waypoint import *

# Colors (RGB)
BLACK = (60, 60, 60)
WHITE = (220, 220, 220)
GRAY = (180, 180, 180)


class MapBuilder:
    FPS = 60

    def __init__(self, size: Tuple[int, int], gridnr: int):
        pg.init()
        self.grinnr = gridnr
        self.grid_size = size[0] // self.grinnr
        self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        self.grid = [
            [Cell((self.grid_size, self.grid_size)) for _ in range(0, self.grinnr)]
            for _ in range(0, self.grinnr)
        ]

    def export(self):
        pass

    def run(self):
        mouse_x = 0
        mouse_y = 0
        running = True
        print("Welcome to MapBuilder")
        print("Press <X> to export current map")
        while running:
            self.clock.tick(self.FPS)

            for ev in pg.event.get():
                match ev.type:
                    case pg.QUIT:
                        running = False
                    case pg.KEYDOWN:
                        if ev.key == pg.K_x:
                            print("Exporting current map")
                            self.export()

            x, y = pg.mouse.get_pos()

            for i in range(self.grinnr):
                for j in range(self.grinnr):
                    self.grid[i][j].fill(BLACK)

            mouse_x, mouse_y = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()
            i = mouse_y // self.grid_size
            j = mouse_x // self.grid_size
            if mouse_clicked[0]:  # left click
                self.grid[i][j].set_enabled(True)
            elif mouse_clicked[2]:  # right click
                self.grid[i][j].set_enabled(False)

            sx = sy = 0
            for i in range(self.grinnr):
                sx = 0
                for j in range(self.grinnr):
                    if self.grid[i][j].enabled:
                        self.grid[i][j].fill(WHITE)
                    self.screen.blit(self.grid[i][j], (sx, sy))
                    sx += self.grid_size
                sy += self.grid_size

            for x in range(0, WIDTH, self.grid_size):
                pg.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, self.grid_size):
                pg.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))
            pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    WIDTH = HEIGHT = 600
    map_builder = MapBuilder((WIDTH, HEIGHT), 30)
    map_builder.run()
