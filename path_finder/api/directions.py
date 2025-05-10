import os
import googlemaps
from datetime import datetime

class DirectionsAPI:
    def __init__(self):
        self.client = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
    
    def get_route_polyline(self, origin, destination):
        """Get road-aligned polyline between two points.
        
        Args:
            origin: [lat, lng] coordinates as a list or tuple
            destination: [lat, lng] coordinates as a list or tuple
            
        Returns:
            Encoded polyline string or None if request fails
        """
        try:
            # Format coordinates as strings for the API
            origin_str = f"{origin[0]},{origin[1]}"
            dest_str = f"{destination[0]},{destination[1]}"
            
            directions = self.client.directions(
                origin=origin_str,
                destination=dest_str,
                mode="driving",
                departure_time=datetime.now()
            )
            
            if directions and len(directions) > 0:
                return directions[0]['overview_polyline']['points']
            else:
                print(f"No directions found between {origin_str} and {dest_str}")
                return None
                
        except Exception as e:
            print(f"Directions API Error: {str(e)}")
            return None 