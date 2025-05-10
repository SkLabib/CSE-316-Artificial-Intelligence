import os
import folium
import pandas as pd
import polyline
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import DirectionsAPI
from api.directions import DirectionsAPI

def test_directions_api():
    """Test the DirectionsAPI and visualize a road-aligned route."""
    print("Testing DirectionsAPI with sample coordinates...")
    
    # Create a sample DataFrame with locations
    locations_df = pd.DataFrame({
        'address': [
            'Empire State Building, New York, NY',
            'Times Square, New York, NY',
            'Central Park, New York, NY',
            'Brooklyn Bridge, New York, NY',
            'Statue of Liberty, New York, NY'
        ],
        'lat': [40.7484, 40.7580, 40.7851, 40.7061, 40.6892],
        'lng': [-73.9857, -73.9855, -73.9683, -73.9969, -74.0445]
    })
    
    # Initialize DirectionsAPI
    directions_api = DirectionsAPI()
    
    # Create a map centered on New York
    m = folium.Map(location=[40.7580, -73.9855], zoom_start=12)
    
    # Add markers for each location
    for idx, row in locations_df.iterrows():
        folium.Marker(
            location=[row['lat'], row['lng']],
            popup=row['address'],
            icon=folium.Icon(icon="info-sign")
        ).add_to(m)
    
    # Test getting directions between locations
    success_count = 0
    for i in range(len(locations_df) - 1):
        # Get origin and destination coordinates
        origin = locations_df.iloc[i][['lat', 'lng']].values
        dest = locations_df.iloc[i+1][['lat', 'lng']].values
        
        print(f"Getting directions from {locations_df.iloc[i]['address']} to {locations_df.iloc[i+1]['address']}...")
        
        # Get road-aligned polyline
        encoded_polyline = directions_api.get_route_polyline(origin, dest)
        
        if encoded_polyline:
            success_count += 1
            print(f"  ✓ Received polyline: {encoded_polyline[:30]}...")
            
            # Decode the polyline to get coordinates
            route_coords = polyline.decode(encoded_polyline)
            
            # Add the polyline to the map
            folium.PolyLine(
                locations=route_coords,
                color='blue',
                weight=3,
                opacity=0.7,
                tooltip=f"Route {i+1}: {locations_df.iloc[i]['address']} to {locations_df.iloc[i+1]['address']}"
            ).add_to(m)
        else:
            print(f"  ✗ Failed to get directions")
            
            # Add a straight line as fallback
            folium.PolyLine(
                [[origin[0], origin[1]], [dest[0], dest[1]]],
                color='red',
                weight=2,
                opacity=0.5,
                dash_array='5, 5'
            ).add_to(m)
    
    # Save the map to an HTML file
    output_file = "directions_test_map.html"
    m.save(output_file)
    
    print(f"\nTest summary: {success_count}/{len(locations_df)-1} routes successfully retrieved")
    print(f"Map saved to {output_file}")
    
    return success_count, len(locations_df)-1

if __name__ == "__main__":
    test_directions_api() 