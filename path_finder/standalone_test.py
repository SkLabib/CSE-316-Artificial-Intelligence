import pandas as pd
import numpy as np
import time
import os
import folium
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules
from utils.graph import GraphBuilder
from algorithms.genetic_algorithm import GeneticAlgorithm
from api.directions import DirectionsAPI
from gui.map_visualization import MapVisualization

def get_sample_data():
    """Generate sample data for testing."""
    # Sample addresses and locations
    locations_df = pd.DataFrame({
        'address': [
            '123 Main St, New York, NY',
            '456 Broadway, New York, NY',
            '789 Fifth Avenue, New York, NY',
            '101 Park Avenue, New York, NY',
            '202 Washington St, New York, NY'
        ],
        'lat': [40.7128, 40.7589, 40.7829, 40.7549, 40.7399],
        'lng': [-74.0060, -73.9851, -73.9654, -73.9749, -73.9903]
    })
    
    # Generate distance matrix (in meters)
    n = len(locations_df)
    distances = np.zeros((n, n))
    durations = np.zeros((n, n))
    
    # Fill matrices with sample data
    for i in range(n):
        for j in range(n):
            if i != j:
                # Calculate distance based on lat/lng (rough approximation)
                lat1, lng1 = locations_df.iloc[i]['lat'], locations_df.iloc[i]['lng']
                lat2, lng2 = locations_df.iloc[j]['lat'], locations_df.iloc[j]['lng']
                
                # Simple Euclidean distance in degrees, converted to meters
                dist = np.sqrt((lat2-lat1)**2 + (lng2-lng1)**2) * 111000  # 1 degree ≈ 111 km
                distances[i, j] = dist
                
                # Estimate duration (assuming 30 km/h average speed)
                durations[i, j] = dist / (30 * 1000 / 3600)  # Result in seconds
    
    return locations_df, distances, durations

def main():
    """Main test function."""
    print("Starting standalone test...")
    
    # Get sample data
    print("Generating sample data...")
    locations_df, distances, durations = get_sample_data()
    print(f"Created sample data with {len(locations_df)} locations")
    
    try:
        # Initialize GraphBuilder
        print("Initializing GraphBuilder...")
        graph_builder = GraphBuilder(
            locations_df,
            distances,
            durations
        )
        
        # Check if locations are properly initialized
        print(f"GraphBuilder.locations: {graph_builder.locations}")
        
        # Build the graph
        print("Building graph...")
        graph_builder.build_complete_graph()
        print("Graph built successfully!")
        
        # Initialize Genetic Algorithm
        print("Initializing Genetic Algorithm...")
        ga = GeneticAlgorithm(
            graph_builder,
            population_size=50,
            generations=20,
            crossover_prob=0.8,
            mutation_prob=0.2
        )
        
        # Run optimization
        print("Running optimization...")
        start_time = time.time()
        result = ga.optimize()
        end_time = time.time()
        
        # Print results
        print("\nOptimization Results:")
        print(f"Best path: {result['path']}")
        print(f"Total distance: {result['distance']:.2f} meters")
        print(f"Total duration: {result['duration']:.2f} seconds")
        print(f"Computation time: {result['computation_time']:.2f} seconds")
        print(f"Total wall time: {end_time - start_time:.2f} seconds")
        
        # Test the MapVisualization with road-aligned routes
        print("\nTesting MapVisualization with road-aligned routes...")
        map_vis = MapVisualization()
        
        # Create a list of algorithm results (just the GA result for now)
        algorithm_results = [result]
        
        # Create a map (without Streamlit)
        m = folium.Map(location=[locations_df['lat'].mean(), locations_df['lng'].mean()], 
                      zoom_start=12)
        
        # Add markers for each location
        for idx, row in locations_df.iterrows():
            folium.Marker(
                location=[row['lat'], row['lng']],
                popup=row['address'],
                icon=folium.Icon(icon="info-sign")
            ).add_to(m)
        
        # Add road-aligned routes
        for result in algorithm_results:
            path = result['path']
            map_vis._add_road_route(m, path, locations_df, 'blue')
        
        # Save the map
        output_file = "optimized_route_map.html"
        m.save(output_file)
        print(f"Map with road-aligned routes saved to {output_file}")
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main() 