import pygame
import sys
from grid_world import GridWorld
from path_planner import generate_coverage_path, astar
from robot_state import Robot

# Constants
CELL_SIZE = 25
GRID_W, GRID_H = 30, 20
PANEL_W = 350
WIDTH, HEIGHT = (GRID_W * CELL_SIZE) + PANEL_W, GRID_H * CELL_SIZE
FPS = 15 

# Colors
GRAY = (200, 200, 200)
GREEN = (100, 255, 100)
RED = (255, 50, 50)
BLACK = (40, 40, 40)
BLUE = (50, 100, 255)
WHITE = (255, 255, 255)
DARK_GRAY = (30, 30, 30)
TEXT_COLOR = (220, 220, 220)

def draw_grid(screen, world):
    for x in range(world.width):
        for y in range(world.height):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell = world.get_cell(x, y)
            
            color = GRAY
            if cell.is_obstacle:
                color = BLACK
            elif cell.is_flagged:
                color = RED
            elif cell.is_covered:
                color = GREEN
                
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, DARK_GRAY, rect, 1) # Grid lines

def draw_dashboard(screen, font, robot, world):
    panel_rect = pygame.Rect(GRID_W * CELL_SIZE, 0, PANEL_W, HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, panel_rect)
    
    # State & Telemetry
    texts = [
        "AMDS TELEMETRY DASHBOARD",
        "-"*30,
        f"ROBOT STATE: {robot.state}",
        f"POSITION: ({robot.x}, {robot.y})",
        "-"*30,
        f"GPR CONFIDENCE: {robot.current_gpr}",
        f"CV CONFIDENCE:  {robot.current_cv}",
        f"FUSED THREAT:   {robot.current_fused}",
        "-"*30,
        "ACTIVE THREAT ALERTS:"
    ]
    
    y_offset = 20
    for text in texts:
        color = RED if "THREAT_HALT" in text else TEXT_COLOR
        surface = font.render(text, True, color)
        screen.blit(surface, (GRID_W * CELL_SIZE + 20, y_offset))
        y_offset += 25
        
    # Log display
    for alert in robot.alert_log[-8:]: # Show last 8 alerts
        log_txt = f"[{alert['time']}] C:{alert['coord']} F:{alert['fused']}"
        surface = font.render(log_txt, True, RED)
        screen.blit(surface, (GRID_W * CELL_SIZE + 20, y_offset))
        y_offset += 20

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AMDS - Autonomous Sweeping Simulation")
    font = pygame.font.SysFont("courier", 16, bold=True)
    clock = pygame.time.Clock()

    world = GridWorld(GRID_W, GRID_H, num_obstacles=50, num_threats=12)
    robot = Robot(0, 0)
    
    # Generate Boustrophedon plan
    global_plan = generate_coverage_path(GRID_W, GRID_H)
    current_path_queue = []
    
    running = True
    mission_complete = False

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not mission_complete:
            if robot.state == "THREAT_HALT":
                robot.halt_timer -= 1
                if robot.halt_timer <= 0:
                    robot.state = "MOVING"
            else:
                if not current_path_queue:
                    # Find the next valid target in the global plan
                    while global_plan:
                        target = global_plan.pop(0)
                        if world.get_cell(*target).is_obstacle:
                            continue
                        # Use A* to navigate to the next valid lawnmower target
                        route = astar(world, (robot.x, robot.y), target)
                        if route:
                            current_path_queue = route
                            break

                if current_path_queue:
                    next_step = current_path_queue.pop(0)
                    robot.x, robot.y = next_step
                    
                    # Sense the new cell
                    cell = world.get_cell(robot.x, robot.y)
                    if not cell.is_covered:
                        robot.sense_cell(cell)
                else:
                    if not global_plan:
                        mission_complete = True
                        robot.state = "MISSION_COMPLETE"

        # Render
        draw_grid(screen, world)
        
        # Draw Robot
        rx = int(robot.x * CELL_SIZE + CELL_SIZE/2)
        ry = int(robot.y * CELL_SIZE + CELL_SIZE/2)
        pygame.draw.circle(screen, BLUE, (rx, ry), int(CELL_SIZE/2.5))
        
        draw_dashboard(screen, font, robot, world)
        
        pygame.display.flip()
        clock.tick(FPS)

    # End of run summary
    print("\n--- MISSION SUMMARY ---")
    print(f"Total Area Swept: {GRID_W * GRID_H} cells")
    print(f"Threats Neutralized: {len(robot.alert_log)}")
    for alert in robot.alert_log:
        print(f"Location: {alert['coord']} | Fused Confidence: {alert['fused']}")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()