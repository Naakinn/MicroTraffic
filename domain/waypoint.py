from dataclasses import dataclass
from enum import Enum
from typing import Any
from .entities import DirectionType, Intersection

class WaypointType(Enum):
    ROAD = "ROAD"
    WALL = "WALL"
    INTERSECTION = "INTERSECTION"
    TRAFFIC_LIGHT = "TRAFFIC_LIGHT"


@dataclass
class Waypoint:
    x: int
    y: int
    type: WaypointType
    RADIUS = 10
    holder: Any = None


def waypoint_factory(type: WaypointType, holder: Any = None) -> Any:
    def create_waypoint(x: int, y: int):
        nonlocal type
        nonlocal holder
        return Waypoint(type=type, x=x, y=y, holder=holder)

    return create_waypoint


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
