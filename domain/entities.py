from dataclasses import dataclass
from enum import Enum, auto

import pygame as pg


class DirectionType(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class CellType(Enum):
    R = auto()
    W = auto()
    UI = auto()
    RI = auto()
    DI = auto()
    LI = auto()
    UL = auto()
    UR = auto()
    DR = auto()
    DL = auto()
    LIGHT = auto


class Cell(pg.surface.Surface):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.type: CellType = CellType.W

    def set_type(self, type: CellType):
        self.type = type


@dataclass
class Block:
    size: int
    type: CellType
