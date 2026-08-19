import time
from sensors import read_gpr, read_cv
from fusion import fuse_scores, classify

class Robot:
    def __init__(self, start_x: int, start_y: int):
        self.x = start_x
        self.y = start_y
        self.state = "MOVING"
        self.alert_log = []
        self.halt_timer = 0
        
        # Live dashboard stats
        self.current_gpr = 0.0
        self.current_cv = 0.0
        self.current_fused = 0.0

    def sense_cell(self, cell):
        self.state = "SENSING"
        self.current_gpr = read_gpr(cell)
        self.current_cv = read_cv(cell)
        self.current_fused = fuse_scores(self.current_gpr, self.current_cv)
        
        classification = classify(self.current_fused)
        cell.is_covered = True
        
        if classification == "THREAT":
            self.state = "THREAT_HALT"
            cell.is_flagged = True
            self.alert_log.append({
                "coord": (self.x, self.y),
                "gpr": self.current_gpr,
                "cv": self.current_cv,
                "fused": self.current_fused,
                "time": time.strftime("%H:%M:%S")
            })
            self.halt_timer = 15  # Freeze for 15 frames to simulate stop
        else:
            self.state = "MOVING"