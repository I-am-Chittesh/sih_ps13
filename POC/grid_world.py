import random
from dataclasses import dataclass

@dataclass
class Cell:
    x: int
    y: int
    is_obstacle: bool = False
    is_threat: bool = False
    is_covered: bool = False
    is_flagged: bool = False

class GridWorld:
    def __init__(self, width: int = 30, height: int = 20, num_obstacles: int = 40, num_threats: int = 8):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]
        self._seed_environment(num_obstacles, num_threats)

    def _seed_environment(self, num_obstacles, num_threats):
        available_cells = [(x, y) for x in range(self.width) for y in range(self.height)]
        if (0, 0) in available_cells:
            available_cells.remove((0, 0))
            
        random.shuffle(available_cells)

        for _ in range(num_obstacles):
            if not available_cells: break
            x, y = available_cells.pop()
            self.grid[x][y].is_obstacle = True

        for _ in range(num_threats):
            if not available_cells: break
            x, y = available_cells.pop()
            self.grid[x][y].is_threat = True

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[x][y]

    def is_valid_move(self, x: int, y: int) -> bool:
        if 0 <= x < self.width and 0 <= y < self.height:
            return not self.grid[x][y].is_obstacle
        return False