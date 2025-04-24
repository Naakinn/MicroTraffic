from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List


class WaypointType(Enum):
    ROAD = "ROAD"
    WALL = "WALL"
    INTERSECTION = "INTERSECTION"
    TRAFFIC_LIGHT = "TRAFFIC_LIGHT"


class DirectionType(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


@dataclass
class Intersection:
    directions: List[DirectionType]


@dataclass
class Waypoint:
    x: int
    y: int
    type: WaypointType
    RADIUS = 10
    holder: Any = None
