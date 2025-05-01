from typing import List, Tuple

import pygame as pg

from domain.entities import DirectionType
from domain.map import load_image
from domain.vehicle import Vehicle


class SimulationEngine:
    FPS = 60

    def __init__(self, pathname: str, size: Tuple[int, int]):
        pg.init()
        self.screen = pg.display.set_mode(size)
        self.clock = pg.time.Clock()

        # Game objects
        self.vehicles: List[Vehicle] = []
        self.map = load_image(pathname)

    def usage(self):
        print("Welcome to MicroTraffic sumulation")
        print("Press <SPACE> to pause")
        print("Press <R> to restart")
        print("Press <N> to add new vehicle")

    def add_vehicle(self):
        # TODO change spawn points
        x, y = 9, 45
        self.vehicles.append(Vehicle(x, y, DirectionType.RIGHT))

    def mainloop(self):
        pause = False
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
                                print(f"Pause = {pause}")
                            case pg.K_r:
                                print("Restarted")
                                return 1
                            case pg.K_n:
                                self.add_vehicle()

            # Update state
            if not pause:
                for vehicle in self.vehicles:
                    vehicle.move()

            # Draw & Update
            self.screen.blit(self.map, (0, 0))
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
        while self.mainloop():
            self.vehicles.clear()
        pg.quit()


if __name__ == "__main__":
    sim = SimulationEngine("res/city_map.png", (400, 400))
    sim.run()
