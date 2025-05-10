import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class GraphBuilder:
    def __init__(self, locations=None, distance_matrix=None, duration_matrix=None):
        # Store original DataFrame
        self.locations_df = locations
        
        # ✅ Ensure this line exists to initialize `locations` as a list
        if locations is not None:
            self.locations = locations[['lat', 'lng']].values.tolist()
        else:
            self.locations = None
        
        self.distance_matrix = distance_matrix
        self.duration_matrix = duration_matrix
        self.graph = None
    
    def build_complete_graph(self, weight_type='distance'):
        """
        Build a complete graph where each node is connected to every other node.
        
        Parameters:
            weight_type (str): 'distance' or 'duration' to determine which matrix to use for edge weights
        
        Returns:
            networkx.Graph: Complete graph with all locations connected
        """
        if self.locations_df is None or self.distance_matrix is None:
            raise ValueError("Locations and distance matrix must be set before building graph")
        
        # Create an empty undirected graph
        G = nx.Graph()
        
        # Add nodes with attributes
        for i, row in self.locations_df.iterrows():
            G.add_node(i, 
                      pos=(row['lng'], row['lat']),  # Geographic position
                      address=row['address'],
                      lat=row['lat'],
                      lng=row['lng'])
        
        # Add edges with weights
        n = len(self.locations_df)
        for i in range(n):
            for j in range(i+1, n):  # Only add edges once (undirected graph)
                if weight_type == 'distance':
                    weight = self.distance_matrix[i, j]
                elif weight_type == 'duration':
                    weight = self.duration_matrix[i, j]
                else:
                    raise ValueError("weight_type must be 'distance' or 'duration'")
                
                G.add_edge(i, j, 
                          weight=weight,
                          distance=self.distance_matrix[i, j], 
                          duration=self.duration_matrix[i, j])
        
        self.graph = G
        return G
    
    def get_node_positions(self):
        """Get node positions for visualization."""
        if self.graph is None:
            raise ValueError("Graph must be built before getting positions")
        
        return {node: data['pos'] for node, data in self.graph.nodes(data=True)}
    
    def visualize_graph(self, figsize=(10, 8), save_path=None):
        """Visualize the graph with weighted edges."""
        if self.graph is None:
            raise ValueError("Graph must be built before visualization")
        
        # Get positions and prepare for plotting
        pos = self.get_node_positions()
        
        # Create figure
        plt.figure(figsize=figsize)
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, node_size=300, node_color='skyblue')
        
        # Draw edges with varying thickness based on weight
        weights = [data['weight']/max([data['weight'] for _, _, data in self.graph.edges(data=True)]) 
                   for _, _, data in self.graph.edges(data=True)]
        nx.draw_networkx_edges(self.graph, pos, width=weights, alpha=0.7)
        
        # Draw labels
        label_pos = {k: (v[0], v[1] + 0.02) for k, v in pos.items()}  # Offset labels slightly
        labels = {node: self.graph.nodes[node]['address'].split(',')[0] for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, label_pos, labels=labels, font_size=8)
        
        plt.title("Delivery Locations Network")
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return plt.gcf()
    
    def get_path_length(self, path, weight='weight'):
        """Calculate the total length (distance or time) of a path."""
        if self.graph is None:
            raise ValueError("Graph must be built before calculating path length")
        
        total = 0
        for i in range(len(path) - 1):
            total += self.graph[path[i]][path[i+1]][weight]
        
        # If the path should return to the starting point (complete TSP)
        # total += self.graph[path[-1]][path[0]][weight]
        
        return total 