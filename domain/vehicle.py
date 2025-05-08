import random
from math import sqrt
from typing import List, Tuple

from .entities import Block, CellType, DirectionType


class Vehicle:
    RADIUS = 12
    DETECTION_DISTANCE = 1
    MAX_TURNS = 2

    def __init__(
        self,
        x: int,
        y: int,
        block_size: int,
        grid: List[List[Block]],
        direction: DirectionType,
    ) -> None:
        self.x: int = x
        self.y: int = y
        self.vx: int = 0
        self.vy: int = 0
        self.max_vel: int = 1
        self.turns: int = 0
        self.block_size: int = block_size
        self.grid: List[List[Block]] = grid
        self.current_block: Block | None = None
        self.block_detected: bool = False
        self.direction: DirectionType | None = None
        self.color: Tuple[int, int, int] = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200),
        )

        self.update_current_block()
        self.set_direction(direction)

    def set_direction(self, direction: DirectionType):
        if self.turns > self.MAX_TURNS:
            return
        if self.direction != direction:
            self.turns += 1
        self.block_detected = True
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

    def update_current_block(self):
        i = self.y // self.block_size
        j = self.x // self.block_size
        if 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0]):
            if self.current_block != self.grid[i][j]:
                self.block_detected = False
            self.current_block = self.grid[i][j]
        else:
            self.current_block = None

    def match_direction(self, type: CellType):
        match type:
            case CellType.UI:
                self.set_direction(DirectionType.UP)
            case CellType.RI:
                self.set_direction(DirectionType.RIGHT)
            case CellType.DI:
                self.set_direction(DirectionType.DOWN)
            case CellType.LI:
                self.set_direction(DirectionType.LEFT)
            case CellType.DL:
                self.set_direction(
                    random.choice((DirectionType.DOWN, DirectionType.LEFT))
                )
            case CellType.UL:
                self.set_direction(
                    random.choice((DirectionType.UP, DirectionType.LEFT))
                )
            case CellType.UR:
                self.set_direction(
                    random.choice((DirectionType.UP, DirectionType.RIGHT))
                )
            case CellType.DR:
                self.set_direction(
                    random.choice((DirectionType.DOWN, DirectionType.RIGHT))
                )

    def update_direction(self, light_state: bool):
        if self.current_block is None:
            self.stop()
            return
        match self.current_block.type:  # type: ignore
            case CellType.R:
                self.turns = 0
            case CellType.W:
                self.stop()
            case CellType.LIGHT:
                if not light_state:
                    self.vx = self.vy = 0
                else:
                    self.set_direction(self.direction)  # type: ignore
            case _:
                center_x = (
                    self.x // self.block_size
                ) * self.block_size + self.block_size // 2
                center_y = (
                    self.y // self.block_size
                ) * self.block_size + self.block_size // 2
                if (
                    not self.block_detected
                    and (center_x - self.x) ** 2 + (center_y - self.y) ** 2
                    <= self.DETECTION_DISTANCE**2
                ):
                    self.match_direction(self.current_block.type)  # type: ignore

    def move(self, light_state: bool):
        self.x += self.vx
        self.y += self.vy
        self.update_current_block()
        self.update_direction(light_state)

    def collide(self, vehicles: List["Vehicle"]):
        for vehicle in vehicles:
            if vehicle != self:
                d = round(sqrt((vehicle.x - self.x) ** 2 + (vehicle.y - self.y) ** 2))
                d -= self.RADIUS * 2
                if (d < 0):
                    self.x -= self.vx
                    self.y -= self.vy
