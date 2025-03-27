def is_valid_move(grid, x, y, visited):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] == 0 and (x, y) not in visited

def dfs(grid, start, target, depth, visited, path):
    if start == target:
        path.append(start)
        return True
    
    if depth == 0:
        return False
    
    visited.add(start)
    
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dx, dy in directions:
        nx, ny = start[0] + dx, start[1] + dy
        if is_valid_move(grid, nx, ny, visited):
            path.append((nx, ny))
            if dfs(grid, (nx, ny), target, depth - 1, visited, path):
                return True
            path.pop() 
    
    visited.remove(start)
    return False

def iddfs(grid, start, target):
    max_depth = len(grid) * len(grid[0])
    for depth in range(max_depth + 1):
        visited = set()
        path = [start]
        if dfs(grid, start, target, depth, visited, path):
            return (True, path)
    
    return (False, [])

def solve_maze(grid, start, target):
    found, path = iddfs(grid, start, target)
    if found:
        print(f"Path found at depth {len(path) - 1} using IDDFS")
        print("Traversal Order:", path)
    else:
        print(f"Path not found at max depth {len(grid) * len(grid[0])} using IDDFS")

# Example Case 1
grid1 = [
    [0, 0, 1, 0],
    [1, 0, 1, 0],
    [0, 0, 0, 0],
    [1, 1, 0, 1]
]
start1 = (0, 0)
target1 = (2, 3)
solve_maze(grid1, start1, target1)

# Example Case 2
grid2 = [
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0]
]
start2 = (0, 0)
target2 = (2, 2)
solve_maze(grid2, start2, target2)
