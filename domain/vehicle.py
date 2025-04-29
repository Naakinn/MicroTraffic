import random
from typing import Tuple

from .entities import DirectionType, Waypoint, WaypointType
from .map import GRIDNR, GRIDSIZE, grid


class Vehicle:
    RADIUS = 8
    WAYPOINT_DISTANCE = 10
    DETECTION_DISTANCE = 2
    MAX_TURNS = 2

    def __init__(self, x: int, y: int, direction: DirectionType) -> None:
        self.x: int = x
        self.y: int = y
        self.vx: int = 0
        self.vy: int = 0
        self.max_vel: int = 1
        self.turns: int = 0
        self.current_waypoint: Waypoint | None = None
        self.waypoint_detected: bool = False
        self.direction: DirectionType | None = None
        self.color: Tuple[int, int, int] = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200),
        )
        self.update_current_waypoint()
        self.set_direction(direction)

    def set_direction(self, direction: DirectionType):
        if self.turns >= self.MAX_TURNS:
            return
        if self.direction != direction:
            self.turns += 1
        self.waypoint_detected = True
        self.direction = direction
        match self.direction:
            case DirectionType.UP:
                self.vx = 0
                self.vy = -self.max_vel
            case DirectionType.DOWN:
                self.vx = 0
                self.vy = self.max_vel
            case DirectionType.LEFT:
                self.vx = -self.max_vel
                self.vy = 0
            case DirectionType.RIGHT:
                self.vx = self.max_vel
                self.vy = 0

    def stop(self):
        self.direction = None
        self.vx = self.vy = 0

    def update_current_waypoint(self):
        x_cell = int(self.x // GRIDSIZE)
        y_cell = int(self.y // GRIDSIZE)
        min_dist = 1000**2
        min_wp = None
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                new_x = x_cell + dx
                new_y = y_cell + dy
                if 0 <= new_x < GRIDNR and 0 <= new_y < GRIDNR:
                    for wp in grid[new_y][new_x]:
                        dist = (wp.x - self.x) ** 2 + (wp.y - self.y) ** 2
                        if dist <= self.WAYPOINT_DISTANCE**2 and dist < min_dist:
                            min_dist = dist
                            min_wp = wp

        if self.current_waypoint != min_wp:
            self.waypoint_detected = False
        self.current_waypoint = min_wp

    def update_direction(self):
        if self.current_waypoint is None:
            self.stop()
            return
        match self.current_waypoint.type:
            case WaypointType.INTERSECTION:
                if (
                    not self.waypoint_detected
                    and (self.current_waypoint.x - self.x) ** 2
                    + (self.current_waypoint.y - self.y) ** 2
                    <= self.DETECTION_DISTANCE**2
                ):
                    self.set_direction(
                        random.choice(self.current_waypoint.holder.directions)
                    )
            case WaypointType.WALL:
                self.stop()
            case WaypointType.ROAD:
                self.turns = 0

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.update_current_waypoint()
        self.update_direction()
