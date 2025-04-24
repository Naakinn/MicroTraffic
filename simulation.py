from domain.entities import DirectionType
from domain.vehicle import Vehicle
from domain.map import load_image
from typing import List, Tuple
import pygame as pg


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

    def add_vehicle(self):
        # TODO change spawn points
        x, y = 61, 45
        self.vehicles.append(Vehicle(x, y, DirectionType.RIGHT))

    def run(self):
        self.usage()
        self.add_vehicle()
        pause = False
        running = True
        while running:
            # Tick FPS
            self.clock.tick(self.FPS)

            # Handle events
            for event in pg.event.get():
                match event.type:
                    case pg.QUIT:
                        running = False
                    case pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            pause = not pause
                            print(f"Pause = {pause}")

            # Update state
            if not pause:
                for vehicle in self.vehicles:
                    vehicle.move()

            # Draw & Update
            self.screen.blit(self.map, (0, 0))
            for vehicle in self.vehicles:
                pg.draw.circle(
                    self.screen, vehicle.color, (vehicle.x, vehicle.y), Vehicle.RADIUS
                )
            pg.display.flip()
        pg.quit()


if __name__ == "__main__":
    sim = SimulationEngine("city_map.png", (400, 400))
    sim.run()
