# Hardcoded map
from .entities import Block, BlockType, Intersection, DirectionType
import pygame as pg
from os import path

W = Block(type=BlockType.WALL)
R = Block(type=BlockType.ROAD)
DL = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.DOWN, DirectionType.LEFT]))
DR = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.DOWN, DirectionType.RIGHT]))
UL = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.UP, DirectionType.LEFT]))
UR = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.UP, DirectionType.RIGHT]))
UI = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.UP]))
DI = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.DOWN]))
RI = Block(type=BlockType.INTERSECTION, holder=Intersection([DirectionType.RIGHT]))

road_map = (
    (W, R,  R,  W, W, W, W, W, W, W, W, R,  R,  W, W, R,  R,  W, W, W),
    (R, DL, UL, R, R, R, R, R, R, R, R, DL, UL, W, W, R,  R,  W, W, W),
    (R, DR, UR, R, R, R, R, R, R, R, R, R, UI, W, W, R,  R,  W, W, W),
    (W, R,  R,  W, W, W, W, W, W, W, W, R,  R,  W, W, DI, UL, R, R, R),
)
ROWNR = len(road_map)
COLNR = len(road_map[0])

class ImageLoader:
    def __call__(self, pathname: str) -> pg.Surface:
        return pg.image.load(path.abspath(pathname))

load_image = ImageLoader()
