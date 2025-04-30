from os import path

import pygame as pg

from .waypoint import *


class ImageLoader:
    def __call__(self, pathname: str) -> pg.Surface:
        return pg.image.load(path.abspath(pathname))


load_image = ImageLoader()


road_map = [
    [W, R, R, W, W, W, W, W, W, W, W, R, R, W, W, R, R, W, W, W],
    [R, DL, UL, R, R, R, R, R, R, R, R, DL, UL, W, W, R, R, W, W, W],
    [R, DR, UR, R, R, R, R, R, R, R, R, DR, UI, W, W, R, R, W, W, W],
    [W, R, R, W, W, W, W, W, W, W, W, R, R, W, W, DI, UL, R, R, R],
    [W, DI, UL, R, R, R, R, R, LI, W, W, R, R, W, W, DR, UR, R, R, R],
    [W, DR, UR, R, R, R, R, R, UI, W, W, R, R, W, W, R, R, W, W, W],
    [W, R, R, W, W, W, W, W, W, W, W, R, R, W, W, R, R, W, W, W],
    [W, R, R, W, W, W, W, W, W, W, W, R, R, W, W, R, R, W, W, W],
    [R, DL, UL, R, DL, LI, R, R, R, R, R, DL, UL, R, R, DL, UL, R, R, R],
    [R, RI, UR, R, DR, UR, R, R, R, R, R, RI, UR, R, R, DR, UR, R, R, R],
]
axes = [
    9,
    27,
    44,
    62,
    79,
    97,
    115,
    132,
    149,
    167,
    185,
    204,
    220,
    239,
    256,
    273,
    290,
    309,
    327,
    344,
]
waypoints = []
for i in range(len(road_map)):
    for j in range(len(road_map[i])):
        waypoints.append(road_map[i][j](axes[j], axes[i]))

GRIDNR = 12
# Hardcoded size
GRIDSIZE = 354 // GRIDNR
grid = [[[] for _ in range(GRIDNR)] for _ in range(GRIDNR)]
for wp in waypoints:
    x_cell = wp.x // GRIDSIZE
    y_cell = wp.y // GRIDSIZE
    grid[y_cell][x_cell].append(wp)
