import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import base64
from io import BytesIO
import polyline

# Import the DirectionsAPI
try:
    from path_finder.api.directions import DirectionsAPI
except ImportError:
    from api.directions import DirectionsAPI

class MapVisualization:
    def __init__(self):
        """Initialize the map visualization component."""
        self.color_map = {
            'Genetic Algorithm': 'blue',
            'A* Search': 'red',
            'Q-Learning': 'green'
        }
        self.directions_api = DirectionsAPI()  # Add the DirectionsAPI
    
    def _add_road_route(self, map_obj, path, locations_df, color):
        """Add road-aligned path between locations.
        
        Args:
            map_obj: Folium map object
            path: List of location indices
            locations_df: DataFrame with location data
            color: Color for the route
        """
        for i in range(len(path) - 1):
            # Get origin and destination coordinates
            origin = locations_df.iloc[path[i]][['lat', 'lng']].values
            dest = locations_df.iloc[path[i+1]][['lat', 'lng']].values
            
            # Get road-aligned polyline
            encoded_polyline = self.directions_api.get_route_polyline(origin, dest)
            
            if encoded_polyline:
                # Decode the polyline to get the coordinates
                route_coords = polyline.decode(encoded_polyline)
                
                # Add the polyline to the map
                folium.PolyLine(
                    locations=route_coords,
                    color=color,
                    weight=4,
                    opacity=0.8
                ).add_to(map_obj)
            else:
                # Fallback to straight line if directions API fails
                route_points = [
                    [locations_df.iloc[path[i]]['lat'], locations_df.iloc[path[i]]['lng']],
                    [locations_df.iloc[path[i+1]]['lat'], locations_df.iloc[path[i+1]]['lng']]
                ]
                folium.PolyLine(
                    route_points,
                    color=color,
                    weight=4,
                    opacity=0.8,
                    dash_array='5, 5'  # Dashed line to indicate it's a fallback
                ).add_to(map_obj)
    
    def visualize_routes(self, locations_df, algorithm_results):
        """
        Visualize multiple algorithm routes on a single map.
        
        Args:
            locations_df: DataFrame with location data (lat, lng, address)
            algorithm_results: List of dictionaries with algorithm results
        """
        if locations_df.empty or not algorithm_results:
            st.warning("No data to visualize.")
            return
        
        # Create the base map centered on the mean lat/lng
        center_lat = locations_df['lat'].mean()
        center_lng = locations_df['lng'].mean()
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=12)
        
        # Add markers for all locations
        marker_cluster = MarkerCluster().add_to(m)
        
        for idx, row in locations_df.iterrows():
            popup_text = f"<b>{row['address']}</b>"
            folium.Marker(
                location=[row['lat'], row['lng']],
                popup=popup_text,
                icon=folium.Icon(icon="globe", prefix="fa")
            ).add_to(marker_cluster)
        
        # Add routes for each algorithm using road-aligned paths
        for result in algorithm_results:
            algorithm_name = result['algorithm']
            path = result['path']
            color = self.color_map.get(algorithm_name, 'purple')
            
            # Add the road-aligned route
            self._add_road_route(m, path, locations_df, color)
            
            # Add start and end markers with algorithm name
            start_idx = path[0]
            end_idx = path[-1]
            
            # Start marker
            folium.Marker(
                [locations_df.iloc[start_idx]['lat'], locations_df.iloc[start_idx]['lng']],
                icon=folium.Icon(icon="play", prefix="fa", color=color),
                popup=f"Start: {algorithm_name}"
            ).add_to(m)
            
            # End marker
            folium.Marker(
                [locations_df.iloc[end_idx]['lat'], locations_df.iloc[end_idx]['lng']],
                icon=folium.Icon(icon="flag", prefix="fa", color=color),
                popup=f"End: {algorithm_name}, Distance: {result['distance']:.2f}m"
            ).add_to(m)
        
        # Create a legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 130px; 
                    border:2px solid grey; z-index:9999; background-color:white;
                    padding: 10px; border-radius: 5px;">
        <h4 style="margin-top: 0;">Legend</h4>
        '''
        
        for algorithm, color in self.color_map.items():
            legend_html += f'''
            <div>
                <span style="display:inline-block; width:15px; height:15px; 
                        background-color:{color}; margin-right:5px;"></span>
                {algorithm}
            </div>
            '''
        
        legend_html += '</div>'
        
        m.get_root().html.add_child(folium.Element(legend_html))
        
        # Display the map
        st.subheader("Route Visualization (Road-Aligned)")
        folium_static(m)
        
        return m
    
    def visualize_comparison(self, comparison_df):
        """
        Visualize algorithm performance comparison as a bar chart.
        
        Args:
            comparison_df: DataFrame with algorithm comparison data
        """
        if comparison_df.empty:
            st.warning("No comparison data to visualize.")
            return
        
        st.subheader("Algorithm Performance Comparison")
        
        # Convert string values back to float for plotting
        df_plot = comparison_df.copy()
        df_plot['distance'] = df_plot['distance'].apply(lambda x: float(x.split()[0]))
        df_plot['duration'] = df_plot['duration'].apply(lambda x: float(x.split()[0]))
        df_plot['computation_time'] = df_plot['computation_time'].apply(lambda x: float(x.split()[0]))
        
        # Set up 3 columns for charts
        col1, col2, col3 = st.columns(3)
        
        # Create figures for each metric
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        
        # Plot distance
        algorithms = df_plot['algorithm'].tolist()
        colors = [self.color_map.get(alg, 'purple') for alg in algorithms]
        
        ax1.bar(algorithms, df_plot['distance'], color=colors)
        ax1.set_title('Total Distance (meters)')
        ax1.set_ylabel('Distance (m)')
        ax1.tick_params(axis='x', rotation=45)
        fig1.tight_layout()
        
        # Plot duration
        ax2.bar(algorithms, df_plot['duration'], color=colors)
        ax2.set_title('Total Duration (minutes)')
        ax2.set_ylabel('Duration (min)')
        ax2.tick_params(axis='x', rotation=45)
        fig2.tight_layout()
        
        # Plot computation time
        ax3.bar(algorithms, df_plot['computation_time'], color=colors)
        ax3.set_title('Computation Time (seconds)')
        ax3.set_ylabel('Time (s)')
        ax3.tick_params(axis='x', rotation=45)
        fig3.tight_layout()
        
        # Display the charts in columns
        with col1:
            st.pyplot(fig1)
        
        with col2:
            st.pyplot(fig2)
        
        with col3:
            st.pyplot(fig3)
        
        # Combine the figures for export
        fig_combined, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Copy the content from individual figures to the combined one
        for i, (ax, metric, title, ylabel) in enumerate(zip(
            axes, 
            ['distance', 'duration', 'computation_time'],
            ['Total Distance (meters)', 'Total Duration (minutes)', 'Computation Time (seconds)'],
            ['Distance (m)', 'Duration (min)', 'Time (s)']
        )):
            ax.bar(algorithms, df_plot[metric], color=colors)
            ax.set_title(title)
            ax.set_ylabel(ylabel)
            ax.tick_params(axis='x', rotation=45)
        
        fig_combined.tight_layout()
        
        return fig_combined
    
    def plot_evolution(self, ga_instance):
        """Plot genetic algorithm evolution if available."""
        if hasattr(ga_instance, 'history') and ga_instance.history['best']:
            st.subheader("Genetic Algorithm Evolution")
            
            fig, ax = plt.subplots(figsize=(10, 6))
            generations = range(len(ga_instance.history['best']))
            
            ax.plot(generations, ga_instance.history['best'], 'b-', label='Best Fitness')
            ax.plot(generations, ga_instance.history['avg'], 'r-', label='Average Fitness')
            
            ax.set_title('Genetic Algorithm Evolution')
            ax.set_xlabel('Generation')
            ax.set_ylabel('Fitness (Total Distance)')
            ax.legend()
            ax.grid(True)
            
            st.pyplot(fig)
            return fig
        
        return None
    
    def plot_learning_progress(self, ql_instance):
        """Plot Q-learning progress if available."""
        if hasattr(ql_instance, 'reward_history') and ql_instance.reward_history:
            st.subheader("Q-Learning Progress")
            
            fig = ql_instance.plot_learning_progress(figsize=(10, 6), window_size=50)
            st.pyplot(fig)
            return fig
        
        return None 