import pygame
import sys
from grid_world import GridWorld
from pp import generate_coverage_path, astar
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
YELLOW = (255, 255, 0) # Color for the interactive highlighter

def draw_grid(screen, world, selected_cell):
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
            
            # Draw the yellow targeting box if the user clicks a cell
            if selected_cell == (x, y):
                pygame.draw.rect(screen, YELLOW, rect, 3)

def draw_dashboard(screen, font, robot, world, selected_cell):
    panel_rect = pygame.Rect(GRID_W * CELL_SIZE, 0, PANEL_W, HEIGHT)
    pygame.draw.rect(screen, DARK_GRAY, panel_rect)
    
    # State & Telemetry
    texts = [
        "AMDS TELEMETRY DASHBOARD",
        "-"*30,
        f"ROBOT STATE: {robot.state}",
        f"POSITION: ({robot.x}, {robot.y})",
        "-"*30,
    ]
    
    # NEW: Interactive Cell Inspector Panel
    if selected_cell:
        cx, cy = selected_cell
        cell = world.get_cell(cx, cy)
        status = "UNEXPLORED"
        if cell.is_obstacle: status = "OBSTACLE"
        elif cell.is_flagged: status = "THREAT DETECTED"
        elif cell.is_covered: status = "CLEARED SAFE"
        
        texts.extend([
            "--- CELL INSPECTOR ---",
            f"TARGET COORD: (X:{cx}, Y:{cy})",
            f"STATUS: {status}",
            "-"*30
        ])
    else:
        texts.extend([
            "--- CELL INSPECTOR ---",
            "CLICK GRID TO INSPECT",
            "ANY CELL COORDINATE",
            "-"*30
        ])
        
    texts.extend([
        "ACTIVE THREAT ALERTS:"
    ])
    
    y_offset = 20
    for text in texts:
        # Dynamic coloring for the dashboard text
        color = TEXT_COLOR
        if "THREAT_HALT" in text or "THREAT DETECTED" in text:
            color = RED
        elif "CLEARED SAFE" in text:
            color = GREEN
        elif "CELL INSPECTOR" in text:
            color = YELLOW
            
        surface = font.render(text, True, color)
        screen.blit(surface, (GRID_W * CELL_SIZE + 20, y_offset))
        y_offset += 25
        
    # Log display for the scrolling alert feed
    for alert in robot.alert_log[-7:]: 
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
    selected_cell = None # Tracks the user's mouse click coordinates

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # NEW: Mouse Click Listener
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                # Convert the pixel click into the exact grid matrix coordinate
                grid_x = mouse_x // CELL_SIZE
                grid_y = mouse_y // CELL_SIZE
                
                # Make sure the user clicked on the grid, not the dashboard
                if 0 <= grid_x < GRID_W and 0 <= grid_y < GRID_H:
                    selected_cell = (grid_x, grid_y)

        if not mission_complete:
            if robot.state == "THREAT_HALT":
                robot.halt_timer -= 1
                if robot.halt_timer <= 0:
                    robot.state = "MOVING"
            else:
                if not current_path_queue:
                    while global_plan:
                        target = global_plan.pop(0)
                        if world.get_cell(*target).is_obstacle:
                            continue
                        route = astar(world, (robot.x, robot.y), target)
                        if route:
                            current_path_queue = route
                            break

                if current_path_queue:
                    next_step = current_path_queue.pop(0)
                    robot.x, robot.y = next_step
                    cell = world.get_cell(robot.x, robot.y)
                    if not cell.is_covered:
                        robot.sense_cell(cell)
                else:
                    if not global_plan:
                        mission_complete = True
                        robot.state = "MISSION_COMPLETE"

        # Render Loop
        draw_grid(screen, world, selected_cell)
        
        # Draw Robot
        rx = int(robot.x * CELL_SIZE + CELL_SIZE/2)
        ry = int(robot.y * CELL_SIZE + CELL_SIZE/2)
        pygame.draw.circle(screen, BLUE, (rx, ry), int(CELL_SIZE/2.5))
        
        draw_dashboard(screen, font, robot, world, selected_cell)
        
        pygame.display.flip()
        clock.tick(FPS)

    print("\n--- MISSION SUMMARY ---")
    print(f"Total Area Swept: {GRID_W * GRID_H} cells")
    print(f"Threats Neutralized: {len(robot.alert_log)}")
    for alert in robot.alert_log:
        print(f"Location: {alert['coord']} | Fused Confidence: {alert['fused']}")
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()