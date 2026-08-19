import heapq

def generate_coverage_path(width: int, height: int):
    """Generates a Boustrophedon (lawnmower) path ignoring obstacles."""
    path = []
    for x in range(width):
        if x % 2 == 0:
            for y in range(height):
                path.append((x, y))
        else:
            for y in range(height - 1, -1, -1):
                path.append((x, y))
    return path

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid_world, start, goal):
    """Custom A* implementation to detour around physical obstacles."""
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        cx, cy = current
        neighbors = [(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)]
        
        for next_node in neighbors:
            nx, ny = next_node
            if grid_world.is_valid_move(nx, ny):
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

    if goal not in came_from:
        return [] # No path found

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path