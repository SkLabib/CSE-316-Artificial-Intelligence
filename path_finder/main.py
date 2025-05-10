import streamlit as st
import os
import warnings
from dotenv import load_dotenv
from path_finder.gui.dashboard import Dashboard

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
    st.sidebar.markdown("Made with ❤️ by [Faria Binte Rashid & Shaikh Mohammed Labib]")
    
    # Check if API key is available
    if not check_api_key():
        return
    
    # Initialize and run the dashboard
    dashboard = Dashboard()
    dashboard.run()

if __name__ == "__main__":
    main() 