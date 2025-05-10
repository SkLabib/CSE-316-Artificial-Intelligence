import time
import heapq
import numpy as np
from collections import defaultdict

class AStar:
    def __init__(self, graph_builder):
        """Initialize A* search algorithm for route optimization."""
        self.graph_builder = graph_builder
        self.nodes = None
        self.graph = None
    
    def _heuristic(self, node1, node2):
        """
        Calculate the heuristic between two nodes (straight-line distance).
        Uses the haversine distance as an admissible heuristic.
        """
        lat1, lng1 = self.graph_builder.graph.nodes[node1]['lat'], self.graph_builder.graph.nodes[node1]['lng']
        lat2, lng2 = self.graph_builder.graph.nodes[node2]['lat'], self.graph_builder.graph.nodes[node2]['lng']
        
        # Use haversine distance as heuristic
        return self._haversine_distance(lat1, lng1, lat2, lng2) * 1000  # Convert km to meters
    
    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on earth."""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def _reconstruct_path(self, came_from, current):
        """Reconstruct the path from the start node to the current node."""
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]  # Reverse to get path from start to end
    
    def find_optimal_path(self, start=0):
        """
        Use A* search to find the optimal path to visit all nodes starting from start_node.
        This implementation solves a variation of the Traveling Salesman Problem.
        
        Args:
            start: The index of the starting node (default is the first node)
            
        Returns:
            Dictionary with the result: path, distance, duration, and computation time
        """
        start_time = time.time()
        
        # Prepare graph data
        self.graph = self.graph_builder.graph
        self.nodes = list(self.graph.nodes())
        unvisited = set(self.nodes)
        unvisited.remove(start)
        
        # Initialize the current path with just the start node
        current_path = [start]
        total_distance = 0
        total_duration = 0
        
        # Continue until all nodes are visited
        while unvisited:
            current = current_path[-1]
            
            # Find the next best node to visit
            best_next_node = None
            best_cost = float('inf')
            
            for next_node in unvisited:
                # g(n) - the cost to reach this node
                g_cost = self.graph[current][next_node]['weight']
                
                # h(n) - the heuristic estimate to the goal (remaining unvisited nodes)
                h_cost = 0
                if len(unvisited) > 1:
                    # Estimate the cost to visit all remaining nodes
                    # This is a simple minimum spanning tree heuristic
                    remaining = unvisited.copy()
                    remaining.remove(next_node)
                    min_edges = []
                    
                    for node in remaining:
                        min_edge = float('inf')
                        for other in remaining:
                            if node != other:
                                edge_cost = self.graph[node][other]['weight']
                                min_edge = min(min_edge, edge_cost)
                        if min_edge != float('inf'):
                            min_edges.append(min_edge)
                    
                    if min_edges:
                        h_cost = sum(min_edges)
                
                # f(n) = g(n) + h(n)
                f_cost = g_cost + h_cost
                
                if f_cost < best_cost:
                    best_cost = f_cost
                    best_next_node = next_node
            
            # Add the best node to our path
            current_path.append(best_next_node)
            total_distance += self.graph[current][best_next_node]['weight']
            total_duration += self.graph[current][best_next_node]['duration']
            unvisited.remove(best_next_node)
        
        # Calculate computation time
        computation_time = time.time() - start_time
        
        return {
            'algorithm': 'A* Search',
            'path': current_path,
            'distance': total_distance,
            'duration': total_duration,
            'computation_time': computation_time
        }
    
    def a_star_search(self, start, goal):
        """
        Standard A* search between two points.
        
        This is a helper function for solving the point-to-point pathfinding problem,
        as opposed to the full TSP-like problem solved by find_optimal_path.
        
        Args:
            start: The starting node
            goal: The goal node
            
        Returns:
            Path from start to goal, or None if no path exists
        """
        # The set of nodes already evaluated
        closed_set = set()
        
        # The set of currently discovered nodes that are not evaluated yet
        open_set = {start}
        
        # For each node, which node it can most efficiently be reached from
        came_from = {}
        
        # For each node, the cost of getting from the start node to that node
        g_score = defaultdict(lambda: float('inf'))
        g_score[start] = 0
        
        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. f_score(n) = g_score(n) + heuristic(n)
        f_score = defaultdict(lambda: float('inf'))
        f_score[start] = self._heuristic(start, goal)
        
        # Use a priority queue for efficient retrieval of lowest f_score node
        open_queue = [(f_score[start], start)]
        
        while open_set:
            # Get the node in open_set having the lowest f_score value
            current = heapq.heappop(open_queue)[1]
            
            if current == goal:
                return self._reconstruct_path(came_from, current)
            
            open_set.remove(current)
            closed_set.add(current)
            
            # For all neighbors of the current node
            for neighbor in self.graph.neighbors(current):
                if neighbor in closed_set:
                    continue  # Ignore already evaluated neighbors
                
                # d(current, neighbor) is the weight of the edge from current to neighbor
                # tentative_g_score is the distance from start to the neighbor through current
                tentative_g_score = g_score[current] + self.graph[current][neighbor]['weight']
                
                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score[neighbor]:
                    continue  # This is not a better path
                
                # This path is the best until now. Record it!
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, goal)
                heapq.heappush(open_queue, (f_score[neighbor], neighbor))
        
        return None  # No path was found 