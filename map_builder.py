from typing import Tuple

import pygame as pg

from domain.entities import Cell, CellType
from domain.waypoint import *
from domain.map import load_image

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
        self.cursor_surfaces = []
        self.cursor_surf_types = []

    def load_cursor_surfaces(self):
        road = pg.Surface((self.grid_size, self.grid_size))
        road.fill(WHITE)
        self.cursor_surfaces.append(road)
        for name in ("UI", "RI", "DI", "LI", "UL", "UR", "DR", "DL"):
            self.cursor_surfaces.append(
                pg.transform.scale(
                    load_image("res/" + name + ".png"), (self.grid_size, self.grid_size)
                )
            )
        self.cursor_surf_types = [
            CellType.R,
            CellType.UI,
            CellType.RI,
            CellType.DI,
            CellType.LI,
            CellType.UL,
            CellType.UR,
            CellType.DR,
            CellType.DL,
        ]

    def export(self):
        pass

    def run(self):
        self.load_cursor_surfaces()
        mouse_x = 0
        mouse_y = 0
        running = True
        current_surf_idx = 0
        print("Welcome to MapBuilder")
        print("Press <X> to export current map")
        print("Scroll mouse wheel to select blocks")
        while running:
            self.clock.tick(self.FPS)

            # Handle events
            for ev in pg.event.get():
                match ev.type:
                    case pg.QUIT:
                        running = False
                    case pg.KEYDOWN:
                        if ev.key == pg.K_x:
                            print("Exporting current map")
                            self.export()
                    case pg.MOUSEWHEEL:
                        # Switch cell types
                        current_surf_idx += ev.dict["y"] if ev.dict["y"] > 0 else 0
                        if current_surf_idx >= len(self.cursor_surfaces):
                            current_surf_idx = 0

            for i in range(self.grinnr):
                for j in range(self.grinnr):
                    self.grid[i][j].fill(BLACK)

            mouse_x, mouse_y = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()
            i = mouse_y // self.grid_size
            j = mouse_x // self.grid_size

            # Display current cell type
            self.grid[i][j].blit(self.cursor_surfaces[current_surf_idx], (0, 0))

            if mouse_clicked[0]:  # left click
                self.grid[i][j].set_type(self.cursor_surf_types[current_surf_idx])
            elif mouse_clicked[2]:  # right click
                self.grid[i][j].set_type(CellType.W)
                self.grid[i][j].fill(BLACK)

            # Draw grid cells
            sx = sy = 0
            for i in range(self.grinnr):
                sx = 0
                for j in range(self.grinnr):
                    # Determine cell type
                    match self.grid[i][j].type:
                        case CellType.R:
                            self.grid[i][j].blit(self.cursor_surfaces[0], (0, 0))
                        case CellType.UI:
                            self.grid[i][j].blit(self.cursor_surfaces[1], (0, 0))
                        case CellType.RI:
                            self.grid[i][j].blit(self.cursor_surfaces[2], (0, 0))
                        case CellType.DI:
                            self.grid[i][j].blit(self.cursor_surfaces[3], (0, 0))
                        case CellType.LI:
                            self.grid[i][j].blit(self.cursor_surfaces[4], (0, 0))
                        case CellType.UL:
                            self.grid[i][j].blit(self.cursor_surfaces[5], (0, 0))
                        case CellType.UR:
                            self.grid[i][j].blit(self.cursor_surfaces[6], (0, 0))
                        case CellType.DR:
                            self.grid[i][j].blit(self.cursor_surfaces[7], (0, 0))
                        case CellType.DL:
                            self.grid[i][j].blit(self.cursor_surfaces[8], (0, 0))
                    # Draw cell
                    self.screen.blit(self.grid[i][j], (sx, sy))
                    sx += self.grid_size
                sy += self.grid_size

            # Draw grid borders
            for x in range(0, WIDTH, self.grid_size):
                pg.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, self.grid_size):
                pg.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

            # Update
            pg.display.flip()

    pg.quit()


if __name__ == "__main__":
    WIDTH = HEIGHT = 600
    map_builder = MapBuilder((WIDTH, HEIGHT), 20)
    map_builder.run()
