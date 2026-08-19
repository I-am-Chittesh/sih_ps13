import pygame
import math
import sys

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AMDS - X-Z Planar Scissor Sweep Kinematics")
clock = pygame.time.Clock()

# Colors
BG = (20, 20, 25)
WHITE = (255, 255, 255)
BLUE = (50, 150, 255)
ORANGE = (255, 80, 50)
GRAY = (120, 120, 120)
DARK_GRAY = (40, 40, 45)

# Mechanical Linkage Parameters
L = 150  # Length of each scissor bar
root_x, root_y = WIDTH // 2, HEIGHT - 100

# Initial State
pan_angle = 90      # 90 degrees is facing straight "up" (forward)
scissor_angle = 45  # Angle of extension (15 = fully extended, 75 = fully retracted)

def calc_joint(start_x, start_y, angle_deg, length):
    """Calculates the end (x,y) of a link given start coords, angle, and length."""
    rad = math.radians(angle_deg)
    # Y is inverted in Pygame (0 is at the top)
    return (start_x + length * math.cos(rad), start_y - length * math.sin(rad))

font = pygame.font.SysFont("courier", 16, bold=True)

running = True
while running:
    screen.fill(BG)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    # Key Controls for Live Interactivity
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:  pan_angle += 2
    if keys[pygame.K_RIGHT]: pan_angle -= 2
    if keys[pygame.K_UP]:    scissor_angle = max(15, scissor_angle - 2)
    if keys[pygame.K_DOWN]:  scissor_angle = min(75, scissor_angle + 2)

    # --- KINEMATICS MATH (Four-Bar Rhombus) ---
    p_root = (root_x, root_y)
    
    # Left and Right middle joints branching from the root
    p_left_mid = calc_joint(p_root[0], p_root[1], pan_angle + scissor_angle, L)
    p_right_mid = calc_joint(p_root[0], p_root[1], pan_angle - scissor_angle, L)
    
    # Tip joint converging at the front
    p_tip = calc_joint(p_left_mid[0], p_left_mid[1], pan_angle - scissor_angle, L)

    # --- RENDERING ---
    # Draw chassis base reference
    pygame.draw.rect(screen, DARK_GRAY, (root_x - 100, root_y, 200, 150))
    pygame.draw.rect(screen, GRAY, (root_x - 100, root_y, 200, 150), 3)

    # Draw Scissor Links (The metal bars)
    pygame.draw.line(screen, GRAY, p_root, p_left_mid, 8)
    pygame.draw.line(screen, GRAY, p_root, p_right_mid, 8)
    pygame.draw.line(screen, GRAY, p_left_mid, p_tip, 8)
    pygame.draw.line(screen, GRAY, p_right_mid, p_tip, 8)

    # Draw Mechanical Joints (Pivot pins)
    for joint in [p_root, p_left_mid, p_right_mid, p_tip]:
        pygame.draw.circle(screen, WHITE, (int(joint[0]), int(joint[1])), 8)
        pygame.draw.circle(screen, BG, (int(joint[0]), int(joint[1])), 4)

    # Draw Sensor Array Bracket (Semi-circle at the tip)
    arc_points = []
    arc_radius = 110
    arc_span = 120  # degrees width of the sensor bar
    start_a = pan_angle - arc_span / 2
    end_a = pan_angle + arc_span / 2
    
    for i in range(21):
        a = start_a + (end_a - start_a) * (i / 20)
        ax, ay = calc_joint(p_tip[0], p_tip[1], a, arc_radius)
        arc_points.append((ax, ay))
        
    # Draw the sensor bar and its connection struts
    pygame.draw.lines(screen, ORANGE, False, arc_points, 10)
    pygame.draw.line(screen, GRAY, p_tip, arc_points[5], 4)
    pygame.draw.line(screen, GRAY, p_tip, arc_points[15], 4)

    # UI Overlay
    texts = [
        "AMDS: X-Z PLANAR KINEMATICS",
        "-" * 30,
        f"EXTENSION ANGLE: {90 - scissor_angle}°",
        f"Y-AXIS PAN ANGLE: {pan_angle}°",
        "-" * 30,
        "CONTROLS:",
        "[UP/DOWN]   : Extend/Retract Pantograph",
        "[LEFT/RIGHT]: Pan Sensor Sweep (Y-Axis Hinge)"
    ]
    
    for i, text in enumerate(texts):
        color = ORANGE if "AMDS" in text else WHITE
        surface = font.render(text, True, color)
        screen.blit(surface, (20, 20 + (i * 25)))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()