from .factories import waypoint_factory
from .entities import WaypointType, Intersection, DirectionType
import pygame as pg
from os import path


class ImageLoader:
    def __call__(self, pathname: str) -> pg.Surface:
        return pg.image.load(path.abspath(pathname))


load_image = ImageLoader()

DL = waypoint_factory(
    WaypointType.INTERSECTION,
    holder=Intersection([DirectionType.DOWN, DirectionType.LEFT]),
)
UL = waypoint_factory(
    WaypointType.INTERSECTION,
    holder=Intersection([DirectionType.UP, DirectionType.LEFT]),
)
DR = waypoint_factory(
    WaypointType.INTERSECTION,
    holder=Intersection([DirectionType.DOWN, DirectionType.RIGHT]),
)
UR = waypoint_factory(
    WaypointType.INTERSECTION,
    holder=Intersection([DirectionType.UP, DirectionType.RIGHT]),
)
UI = waypoint_factory(
    WaypointType.INTERSECTION, holder=Intersection([DirectionType.UP])
)
DI = waypoint_factory(
    WaypointType.INTERSECTION, holder=Intersection([DirectionType.DOWN])
)
RI = waypoint_factory(
    WaypointType.INTERSECTION, holder=Intersection([DirectionType.RIGHT])
)
LI = waypoint_factory(
    WaypointType.INTERSECTION, holder=Intersection([DirectionType.LEFT])
)
R = waypoint_factory(WaypointType.ROAD)
W = waypoint_factory(WaypointType.WALL)

road_map = [
    [W, R, R, W, W, W, W, W, W, W, W, R, R, W, W, R, R, W, W, W],
    [R, DL, UL, R, R, R, R, R, R, R, R, DL, UL, W, W, R, R, W, W, W],
    [R, DR, UR, R, R, R, R, R, R, R, R, R, UI, W, W, R, R, W, W, W],
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
