from .entities import WaypointType, Waypoint
from typing import Any


def waypoint_factory(type: WaypointType, holder: Any = None) -> Any:
    def create_waypoint(x: int, y: int):
        nonlocal type
        nonlocal holder
        return Waypoint(type=type, x=x, y=y, holder=holder)

    return create_waypoint
