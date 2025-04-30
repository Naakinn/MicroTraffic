from dataclasses import dataclass
from enum import Enum, auto
from typing import List

import pygame as pg


class DirectionType(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Intersection:
    directions: List[DirectionType]


class Cell(pg.surface.Surface):
    def __init__(self, *args, **kwargs) -> None:
        self.enabled: bool = False
        super().__init__(*args, **kwargs)

    def set_enabled(self, val: bool):
        self.enabled = val
