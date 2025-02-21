import random

class Node:
    def __init__(self, x, y, depth):
        self.x = x
        self.y = y
        self.depth = depth

class DFS:
    def __init__(self, N):
        self.N = N
        self.grid = self.generate_grid()
        self.directions = [(1, 0, "Down"), (-1, 0, "Up"), (0, 1, "Right"), (0, -1, "Left")]
        self.source, self.goal = self.get_source_and_goal()
        self.found = False
        self.path = []
        self.topological_order = []

    def generate_grid(self):
        return [[random.choice([0, 1]) for _ in range(self.N)] for _ in range(self.N)]
    
    def get_source_and_goal(self):
        free_cells = [(i, j) for i in range(self.N) for j in range(self.N) if self.grid[i][j] == 1]
        source, goal = random.sample(free_cells, 2)
        return Node(source[0], source[1], 0), Node(goal[0], goal[1], float('inf'))

    def print_grid(self):
        for i in range(self.N):
            for j in range(self.N):
                print(self.grid[i][j], end=" ")
            print()
        print()
    
    def dfs(self, x, y, depth):
        if self.found:
            return
        
        self.grid[x][y] = 0  # Mark as visited
        self.topological_order.append((x, y))
        
        for dx, dy, direction in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.N and 0 <= ny < self.N and self.grid[nx][ny] == 1:
                self.path.append(f"Moving {direction} ({nx}, {ny})")
                if (nx, ny) == (self.goal.x, self.goal.y):
                    self.found = True
                    self.goal.depth = depth + 1
                    return
                self.dfs(nx, ny, depth + 1)
                if self.found:
                    return

    def solve(self):
        print("Generated Grid:")
        self.print_grid()
        print(f"Source: ({self.source.x}, {self.source.y})")
        print(f"Goal: ({self.goal.x}, {self.goal.y})")
        
        if self.grid[self.source.x][self.source.y] == 0 or self.grid[self.goal.x][self.goal.y] == 0:
            print("No valid path: Source or Goal is an obstacle.")
            return
        
        self.dfs(self.source.x, self.source.y, 0)
        
        if self.found:
            print("\nDFS Path:")
            print("\n".join(self.path))
            print(f"Goal found in {self.goal.depth} moves.")
            print("\nTopological Order of Traversal:")
            print(self.topological_order)
        else:
            print("Goal cannot be reached.")

if __name__ == "__main__":
    N = random.randint(4, 7)
    solver = DFS(N)
    solver.solve()