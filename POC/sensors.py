import random
from POC.grid_world import Cell

def read_gpr(cell: Cell) -> float:
    if cell.is_threat:
        return round(random.uniform(0.70, 0.99), 2)
    return round(random.uniform(0.05, 0.35), 2)

def read_cv(cell: Cell) -> float:
    if cell.is_threat:
        return round(random.uniform(0.60, 0.95), 2)
    return round(random.uniform(0.00, 0.40), 2)