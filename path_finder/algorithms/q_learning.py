import numpy as np
import time
import matplotlib.pyplot as plt
from collections import defaultdict

class QLearning:
    def __init__(self, graph_builder, learning_rate=0.1, discount_factor=0.9, 
                 exploration_rate=0.1, episodes=1000):
        """Initialize Q-Learning algorithm for route optimization."""
        self.graph_builder = graph_builder
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.episodes = episodes
        self.q_table = None
        self.reward_history = []
    
    def _get_state_key(self, current_node, visited):
        """Create a unique key for a state (current node + visited nodes)."""
        # Convert set of visited nodes to a sorted tuple for hashability
        visited_key = tuple(sorted(visited))
        return (current_node, visited_key)
    
    def _get_reward(self, from_node, to_node, visited, all_nodes):
        """
        Define the reward function:
        - Going to an unvisited node: +10
        - Going to an already visited node: -10
        - Completing the tour (visiting all nodes): +100
        - Step cost based on distance: -distance/1000 (to keep rewards in reasonable range)
        """
        # Base cost (distance-based penalty)
        distance = self.graph_builder.graph[from_node][to_node]['weight']
        step_cost = -distance / 1000  # Scale down to keep rewards manageable
        
        # Is this node already visited?
        if to_node in visited:
            return step_cost - 10  # Penalty for revisiting
        
        # Are we done? (all nodes visited)
        if len(visited) + 1 == len(all_nodes):
            return step_cost + 100  # Big bonus for completing tour
        
        # Normal case - new node
        return step_cost + 10  # Reward for visiting new node
    
    def optimize(self, start=0):
        """Run the Q-learning algorithm to find an optimal path."""
        start_time = time.time()
        
        self.graph = self.graph_builder.graph
        nodes = list(self.graph.nodes())
        num_nodes = len(nodes)
        
        # Initialize Q-table as a nested defaultdict: state -> action -> q-value
        self.q_table = defaultdict(lambda: defaultdict(float))
        
        # Reset reward history
        self.reward_history = []
        
        # Training phase
        for episode in range(self.episodes):
            # Start from the designated node
            current_node = start
            visited = {start}  # Set of visited nodes (including start)
            
            total_reward = 0
            path = [current_node]
            
            # Continue until all nodes are visited or max steps reached
            max_steps = num_nodes * 2  # Allow some backtracking but prevent infinite loops
            step = 0
            
            while len(visited) < num_nodes and step < max_steps:
                # Get current state
                state = self._get_state_key(current_node, visited)
                
                # Choose action using epsilon-greedy policy
                if np.random.random() < self.exploration_rate:
                    # Explore: choose a random neighbor
                    next_node = np.random.choice(list(self.graph.neighbors(current_node)))
                else:
                    # Exploit: choose the best action for this state
                    # If no values yet in the q_table, default to random
                    if not self.q_table[state]:
                        next_node = np.random.choice(list(self.graph.neighbors(current_node)))
                    else:
                        # Choose the action with the highest Q-value
                        next_node = max(self.q_table[state].items(), key=lambda x: x[1])[0]
                
                # Get reward for this action
                reward = self._get_reward(current_node, next_node, visited, nodes)
                total_reward += reward
                
                # Move to next node
                visited.add(next_node)
                path.append(next_node)
                
                # Get new state
                new_state = self._get_state_key(next_node, visited)
                
                # Get max Q value for next state
                max_future_q = max(self.q_table[new_state].values()) if self.q_table[new_state] else 0
                
                # Current Q value
                current_q = self.q_table[state][next_node]
                
                # Q-learning update formula
                new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (
                    reward + self.discount_factor * max_future_q
                )
                
                # Update Q-table
                self.q_table[state][next_node] = new_q
                
                # Move to the next state
                current_node = next_node
                step += 1
            
            # Record rewards for this episode
            self.reward_history.append(total_reward)
            
            # Decay exploration rate
            self.exploration_rate = max(0.01, self.exploration_rate * 0.99)
        
        # Find the best path using the trained Q-table
        best_path = self._get_best_path(start, nodes)
        
        # Calculate distance and duration for the best path
        total_distance = 0
        total_duration = 0
        for i in range(len(best_path) - 1):
            from_node = best_path[i]
            to_node = best_path[i + 1]
            total_distance += self.graph[from_node][to_node]['weight']
            total_duration += self.graph[from_node][to_node]['duration']
        
        computation_time = time.time() - start_time
        
        return {
            'algorithm': 'Q-Learning',
            'path': best_path,
            'distance': total_distance,
            'duration': total_duration,
            'computation_time': computation_time,
            'episodes': self.episodes
        }
    
    def _get_best_path(self, start, nodes):
        """Reconstruct the best path using the trained Q-table."""
        current_node = start
        visited = {start}
        path = [current_node]
        
        while len(visited) < len(nodes):
            state = self._get_state_key(current_node, visited)
            
            # If no Q-values for this state, use a greedy approach
            if not self.q_table[state]:
                # Find the closest unvisited node
                min_distance = float('inf')
                next_node = None
                
                for node in self.graph.neighbors(current_node):
                    if node not in visited and self.graph[current_node][node]['weight'] < min_distance:
                        min_distance = self.graph[current_node][node]['weight']
                        next_node = node
                
                # If all neighbors are visited, choose the closest one
                if next_node is None:
                    next_node = min(
                        self.graph.neighbors(current_node),
                        key=lambda n: self.graph[current_node][n]['weight']
                    )
            else:
                # Choose the best action according to Q-table
                next_node = max(self.q_table[state].items(), key=lambda x: x[1])[0]
            
            visited.add(next_node)
            path.append(next_node)
            current_node = next_node
        
        return path
    
    def plot_learning_progress(self, figsize=(10, 6), window_size=50):
        """Plot the learning progress (rewards over episodes)."""
        plt.figure(figsize=figsize)
        
        # Raw rewards
        plt.plot(self.reward_history, alpha=0.4, color='blue', label='Raw Rewards')
        
        # Moving average for smoothing
        if len(self.reward_history) >= window_size:
            moving_avg = np.convolve(
                self.reward_history, 
                np.ones(window_size)/window_size, 
                mode='valid'
            )
            plt.plot(range(window_size-1, len(self.reward_history)), 
                    moving_avg, color='red', label=f'Moving Avg ({window_size} episodes)')
        
        plt.title('Q-Learning Rewards Over Episodes')
        plt.xlabel('Episode')
        plt.ylabel('Total Reward')
        plt.legend()
        plt.grid(True)
        
        return plt.gcf()
