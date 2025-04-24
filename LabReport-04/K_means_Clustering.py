import random

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster = None

class KMeans:
    def __init__(self, num_points, num_clusters, grid_size=30):
        self.num_points = num_points
        self.num_clusters = num_clusters
        self.grid_size = grid_size
        self.points = [Point(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_points)]
        self.clusters = [Point(random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)) for _ in range(num_clusters)]
        self.run()

    def manhattan_distance(self, p1, p2):
        return abs(p1.x - p2.x) + abs(p1.y - p2.y)

    def assign_clusters(self):
        for point in self.points:
            min_dist = float('inf')
            for idx, cluster in enumerate(self.clusters):
                dist = self.manhattan_distance(point, cluster)
                if dist < min_dist:
                    min_dist = dist
                    point.cluster = idx

    def update_clusters(self):
        for i in range(self.num_clusters):
            members = [p for p in self.points if p.cluster == i]
            if members:
                avg_x = sum(p.x for p in members) // len(members)
                avg_y = sum(p.y for p in members) // len(members)
                self.clusters[i].x = avg_x
                self.clusters[i].y = avg_y

    def has_converged(self, old_clusters):
        return all(c.x == o.x and c.y == o.y for c, o in zip(self.clusters, old_clusters))

    def run(self):
        iterations = 0
        while True:
            self.assign_clusters()
            old_clusters = [Point(c.x, c.y) for c in self.clusters]
            self.update_clusters()
            iterations += 1
            if self.has_converged(old_clusters) or iterations > 100:
                break
        self.visualize()

    def visualize(self):
        matrix = [["." for _ in range(self.grid_size)] for _ in range(self.grid_size)]


        for p in self.points:
            matrix[p.y][p.x] = str(p.cluster)


        for i, c in enumerate(self.clusters):
            matrix[c.y][c.x] = chr(65 + i)  # A, B, C, ...

        print("\n--- 2D Grid Visualization (Cluster IDs and Centers) ---")
        for row in matrix:
            print(" ".join(row))

        print("\n--- Cluster Centers ---")
        for i, c in enumerate(self.clusters):
            print(f"Cluster {i} Center: ({c.x}, {c.y})")

        print("\n--- Cluster Membership ---")
        for i, p in enumerate(self.points):
            print(f"Point {i}: ({p.x}, {p.y}) -> Cluster {p.cluster}")

if __name__ == "__main__":
    kmeans = KMeans(num_points=100, num_clusters=10)
