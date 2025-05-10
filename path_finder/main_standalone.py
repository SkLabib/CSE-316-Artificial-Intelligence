import streamlit as st
import os
import warnings
import sys
import pandas as pd
import numpy as np
from dotenv import load_dotenv

# Add the current directory to the path so we can import local modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Import local modules
from gui.dashboard import Dashboard
from utils.graph import GraphBuilder

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Path Finder - Delivery Route Optimization",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #1E88E5;
    }
    .stButton button {
        background-color: #1E88E5;
        color: white;
    }
    .stProgress .st-bo {
        background-color: #1E88E5;
    }
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
    .stSidebar {
        background-color: #f5f5f5;
    }
</style>
""", unsafe_allow_html=True)

def get_sample_data():
    """Generate sample data for testing the application without API calls."""
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
    
    # Fill matrices with sample data (using Euclidean distance for simplicity)
    for i in range(n):
        for j in range(n):
            if i != j:
                # Calculate distance based on lat/lng (rough approximation)
                lat1, lng1 = locations_df.iloc[i]['lat'], locations_df.iloc[i]['lng']
                lat2, lng2 = locations_df.iloc[j]['lat'], locations_df.iloc[j]['lng']
                
                # Simple Euclidean distance in degrees, converted to meters (very approximate)
                dist = np.sqrt((lat2-lat1)**2 + (lng2-lng1)**2) * 111000  # 1 degree ≈ 111 km
                distances[i, j] = dist
                
                # Estimate duration (assuming 30 km/h average speed)
                # Convert distance from meters to hours: (dist in m) / (30 km/h * 1000 m/km)
                durations[i, j] = dist / (30 * 1000 / 3600)  # Result in seconds
    
    # Convert to DataFrames for compatibility
    indices = list(range(n))
    distance_df = pd.DataFrame(distances, index=indices, columns=indices)
    duration_df = pd.DataFrame(durations, index=indices, columns=indices)
    
    return locations_df, distance_df, duration_df

def check_api_key():
    """Check if the Google Maps API key is available."""
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        st.error("""
        ⚠️ **Google Maps API Key Not Found**
        
        Please make sure you have set up your Google Maps API key in the `.env` file.
        The file should contain a line like:
        
        ```
        GOOGLE_MAPS_API_KEY=your_api_key_here
        ```
        
        If you don't have an API key, you can get one from the 
        [Google Cloud Console](https://console.cloud.google.com/).
        
        Make sure to enable the following APIs:
        - Geocoding API
        - Distance Matrix API
        - Maps Static API
        """)
        return False
    return True

def main():
    """Main application entry point."""
    # Display app title and description
    st.sidebar.image("https://img.icons8.com/color/96/000000/map-marker.png", width=80)
    st.sidebar.title("Path Finder")
    st.sidebar.markdown("""
    **AI-Powered Delivery Route Optimization**
    
    Optimize delivery routes using:
    - Genetic Algorithm
    - A* Search
    - Q-Learning
    
    Using real-world data from Google Maps API.
    """)
    
    # Display credits
    st.sidebar.markdown("---")
    
    
    # Check if API key is available
    if not check_api_key():
        return
    
    # Initialize the dashboard
    dashboard = Dashboard()
    
    # For debugging/development, load sample data into session state
    # This ensures graph_builder can be initialized properly
    use_sample_data = st.sidebar.checkbox("Use Sample Data", value=True)
    
    if use_sample_data:
        st.sidebar.info("Using sample data for testing (no API calls)")
        # Generate and load sample data
        locations_df, distance_df, duration_df = get_sample_data()
        
        # Load into session state
        st.session_state.addresses = locations_df['address'].tolist()
        st.session_state.locations_df = locations_df
        st.session_state.distances = distance_df.values
        st.session_state.durations = duration_df.values
        
        # Directly initialize graph_builder
        dashboard.graph_builder = GraphBuilder(
            locations_df,
            distance_df.values,
            duration_df.values
        )
        dashboard.graph_builder.build_complete_graph()
        st.sidebar.success("Sample data loaded and graph initialized!")
    
    # Run the dashboard
    dashboard.run()

if __name__ == "__main__":
    main() 