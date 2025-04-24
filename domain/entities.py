from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, List

class BlockType(Enum): 
    ROAD          = "ROAD"
    WALL          = "WALL"
    INTERSECTION  = "INTERSECTION"
    TRAFFIC_LIGHT = "TRAFFIC_LIGHT"
    
    def __str__(self) -> str:
        return self.value

class DirectionType(Enum):
    UP    = auto()
    DOWN  = auto()
    LEFT  = auto()
    RIGHT = auto()
    
    def __str__(self) -> str:
        return str(self.value)

@dataclass
class Block: 
    type: BlockType
    SIZE: int = 18
    holder: Any | None = None

@dataclass
class Intersection: 
    directions: List[DirectionType]

        
