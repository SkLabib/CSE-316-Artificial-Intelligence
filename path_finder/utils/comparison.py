import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

class AlgorithmComparison:
    def __init__(self):
        self.results = {
            'algorithm': [],
            'distance': [],
            'duration': [],
            'computation_time': [],
            'path': []
        }
    
    def add_result(self, algorithm_name, path, distance, duration, computation_time):
        """Add a single algorithm's result to the comparison."""
        self.results['algorithm'].append(algorithm_name)
        self.results['distance'].append(distance)
        self.results['duration'].append(duration)
        self.results['computation_time'].append(computation_time)
        self.results['path'].append(path)
    
    def get_comparison_dataframe(self):
        """Convert results to a DataFrame for easy display and analysis."""
        df = pd.DataFrame(self.results)
        
        # Format the columns for better readability
        df['distance'] = df['distance'].apply(lambda x: f"{x:.2f} meters")
        df['duration'] = df['duration'].apply(lambda x: f"{x/60:.2f} minutes")
        df['computation_time'] = df['computation_time'].apply(lambda x: f"{x:.4f} seconds")
        
        # Format path as node sequence
        df['path'] = df['path'].apply(lambda x: ' → '.join(map(str, x)))
        
        return df
    
    def plot_comparison(self, figsize=(12, 6)):
        """Visualize the comparison between algorithms."""
        if not self.results['algorithm']:
            raise ValueError("No results to compare")
        
        # Convert string values back to float for plotting
        distances = [float(d.split()[0]) for d in self.results['distance']]
        durations = [float(d.split()[0]) for d in self.results['duration']]
        comp_times = [float(c.split()[0]) for c in self.results['computation_time']]
        
        # Set up the figure with 3 subplots
        fig, axes = plt.subplots(1, 3, figsize=figsize)
        algorithms = self.results['algorithm']
        
        # Plot distances
        axes[0].bar(algorithms, distances, color='skyblue')
        axes[0].set_title('Total Distance (meters)')
        axes[0].set_ylabel('Distance (m)')
        axes[0].tick_params(axis='x', rotation=45)
        
        # Plot durations
        axes[1].bar(algorithms, durations, color='lightgreen')
        axes[1].set_title('Total Duration (minutes)')
        axes[1].set_ylabel('Duration (min)')
        axes[1].tick_params(axis='x', rotation=45)
        
        # Plot computation times
        axes[2].bar(algorithms, comp_times, color='salmon')
        axes[2].set_title('Computation Time (seconds)')
        axes[2].set_ylabel('Time (s)')
        axes[2].tick_params(axis='x', rotation=45)
        
        # Adjust layout
        plt.tight_layout()
        
        return fig
    
    def best_algorithm(self, criterion='distance'):
        """Determine the best algorithm based on the given criterion."""
        if not self.results['algorithm']:
            raise ValueError("No results to compare")
        
        df = pd.DataFrame(self.results)
        
        # Convert string values back to float for comparison
        if criterion == 'distance':
            df['distance'] = df['distance'].apply(lambda x: float(x.split()[0]))
            best_idx = df['distance'].idxmin()
        elif criterion == 'duration':
            df['duration'] = df['duration'].apply(lambda x: float(x.split()[0]))
            best_idx = df['duration'].idxmin()
        elif criterion == 'computation_time':
            df['computation_time'] = df['computation_time'].apply(lambda x: float(x.split()[0]))
            best_idx = df['computation_time'].idxmin()
        else:
            raise ValueError("Criterion must be 'distance', 'duration', or 'computation_time'")
        
        best_algorithm = df.iloc[best_idx]
        return best_algorithm['algorithm'], best_algorithm 