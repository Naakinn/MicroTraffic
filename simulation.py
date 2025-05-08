from typing import List, Tuple

import pygame as pg
import os
import pickle
import logging

from domain.entities import Block, CellType, DirectionType
from domain.vehicle import Vehicle
from domain.image_loader import image_load

# Colors (RGB)
GREEN = (85, 243, 36)
RED = (240, 20, 20)


class SimulationEngine:
    FPS = 60

    def __init__(self, gridpath: str, surfpath: str, size: Tuple[int, int]):
        pg.init()
        self.grid: List[List[Block]]
        self.grid_size: int
        self.map: pg.Surface
        self.gridpath = gridpath
        self.surfpath = surfpath
        self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()
        self.lights: List[Tuple[Block, int, int]] = []
        self.vehicles: List[Vehicle] = []
        self.current_surf_idx: int = 0
        self.cursor_surfaces: List[pg.Surface] = []
        self.cursor_surf_types: List[CellType] = []
        self.logfile = "simulation.log"
        self.init_logging()

    def init_logging(self):
        logging.basicConfig(filename=self.logfile, level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def usage(self):
        self.logger.debug("Welcome to MicroTraffic Simulation")
        self.logger.debug("Press <SPACE> to pause")
        self.logger.debug("Press <R> to restart")

    def load_cursor_surfaces(self):
        for name in ("UI", "RI", "DI", "LI"):
            self.cursor_surfaces.append(
                pg.transform.scale(
                    image_load("res/" + name + ".png"), (self.grid_size, self.grid_size)
                )
            )
        self.cursor_surf_types = [
            CellType.UI,
            CellType.RI,
            CellType.DI,
            CellType.LI,
        ]

    def import_map(self):
        if not (os.path.exists(self.gridpath) and os.path.exists(self.surfpath)):
            self.logger.error(
                f"'{self.gridpath}' and/or '{self.surfpath}' no such file(s)"
            )
            pg.quit()
            quit(1)

        with open(self.gridpath, "rb") as file:
            self.grid = pickle.load(file)
            self.grid_size = self.grid[0][0].size
        self.logger.info(f"'{self.gridpath}' imported")
        with open(self.surfpath, "rb") as file:
            self.map = pg.surfarray.make_surface(pickle.load(file))
        self.logger.info(f"'{self.surfpath}' imported")

        # Load traffic lights
        x = y = 0
        for row in self.grid:
            x = 0
            for block in row:
                if block.type == CellType.LIGHT:
                    self.lights.append((block, x, y))
                x += self.grid_size
            y += self.grid_size

    def add_vehicle(self, mouse_x: int, mouse_y: int):
        x = (mouse_x // self.grid_size) * self.grid_size + self.grid_size // 2
        y = (mouse_y // self.grid_size) * self.grid_size + self.grid_size // 2
        match self.cursor_surf_types[self.current_surf_idx]:
            case CellType.UI:
                direction = DirectionType.UP
            case CellType.RI:
                direction = DirectionType.RIGHT
            case CellType.DI:
                direction = DirectionType.DOWN
            case _:
                direction = DirectionType.LEFT
        self.vehicles.append(Vehicle(x, y, self.grid_size, self.grid, direction))

    def log(self, light_state: bool):
        open(self.logfile, "w").close()
        for idx, v in enumerate(self.vehicles):
            self.logger.info(
                f"v:{idx + 1}:{v.x}:{v.y}:{'NONE' if v.direction is None else v.direction.value}"
            )
        self.logger.info(f"l:{"GREEN" if light_state else "RED"}")

    def mainloop(self):
        pause = False
        max_cursor_delay_tick = 30
        cursor_delay_tick = 0
        max_light_period_tick = 120
        light_period_tick = 0
        light_state = False  # false - stop, true - go
        while True:
            # Tick FPS
            self.clock.tick(self.FPS)

            # Handle events
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        return 0
                    case pg.KEYDOWN:
                        match event.key:
                            case pg.K_SPACE:
                                pause = not pause
                                if pause:
                                    self.logger.debug("Paused")
                                else:
                                    self.logger.debug("Resumed")
                            case pg.K_r:
                                self.logger.debug("Restarted")
                                return 1
                    case pg.MOUSEWHEEL:
                        self.current_surf_idx += event.dict["y"]
                        if self.current_surf_idx >= len(self.cursor_surfaces):
                            self.current_surf_idx = 0
                        elif self.current_surf_idx < 0:
                            self.current_surf_idx = len(self.cursor_surfaces) - 1

            # Log
            self.log(light_state)
            # Draw map
            self.screen.blit(self.map, (0, 0))

            mouse_x, mouse_y = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()
            self.screen.blit(
                self.cursor_surfaces[self.current_surf_idx],
                (
                    (mouse_x // self.grid_size) * self.grid_size,
                    (mouse_y // self.grid_size) * self.grid_size,
                ),
            )
            if cursor_delay_tick == 0 and mouse_clicked[0]:  # right click
                self.add_vehicle(mouse_x, mouse_y)
                cursor_delay_tick = max_cursor_delay_tick
            if light_period_tick == 0:
                light_state = not light_state
                light_period_tick = max_light_period_tick

            # Update state
            if cursor_delay_tick > 0:
                cursor_delay_tick -= 1

            if not pause:
                for vehicle in self.vehicles:
                    vehicle.move(light_state)
                if light_period_tick > 0:
                    light_period_tick -= 1

            # Draw vehicles & Update
            for _, x, y in self.lights:
                if light_state:
                    pg.draw.rect(
                        self.screen,
                        GREEN,
                        pg.Rect(x, y, self.grid_size, self.grid_size),
                    )
                else:
                    pg.draw.rect(
                        self.screen,
                        RED,
                        pg.Rect(x, y, self.grid_size, self.grid_size),
                    )

            for vehicle in self.vehicles:
                pg.draw.circle(
                    self.screen,
                    vehicle.color,
                    (vehicle.x, vehicle.y),
                    Vehicle.RADIUS,
                )
            pg.display.flip()

    def run(self):
        self.usage()
        self.import_map()
        self.load_cursor_surfaces()
        while self.mainloop():
            self.vehicles.clear()
        pg.quit()


if __name__ == "__main__":
    sim = SimulationEngine("aux/grid.pickle", "aux/surfarray.pickle", (600, 600))
    sim.run()
