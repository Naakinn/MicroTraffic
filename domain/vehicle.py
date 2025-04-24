from .entities import DirectionType, Block
from .map import *
from typing import Tuple
import random

class Vehicle: 
    RADIUS = 8
    def __init__(self, x: int, y: int, direction: DirectionType) -> None:
        self.x: int = x
        self.y: int  = y
        self.vx: int = 0
        self.vy: int = 0
        self.max_vel = 1
        self.direction: DirectionType | None
        self.current_block: Block | None = None
        self.direction_changed: bool = False
        self.color: Tuple[int, int, int] = (
            random.randint(50, 200),
            random.randint(50, 200),
            random.randint(50, 200)
        )
        self.update_current_block()
        self.set_direction(direction)
        
    # TODO update only if vehicle is near to block's center 
    def set_direction(self, direction: DirectionType | None):
        if not self.direction_changed: 
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
        i = self.y // Block.SIZE
        j = self.x // Block.SIZE
        if (i < ROWNR and i >= 0) and (j < COLNR and j >= 0): 
            self.current_block = road_map[i][j]
        else:
            self.stop()
    
    def update_direction(self):
        match self.current_block.type: # type: ignore
            case BlockType.INTERSECTION:
                self.set_direction(random.choice(self.current_block.holder.directions)) # type: ignore
                self.direction_changed = True
            case BlockType.WALL:
                self.stop()
            case BlockType.ROAD:
                self.direction_changed = False
                
    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.update_current_block()
        self.update_direction()

