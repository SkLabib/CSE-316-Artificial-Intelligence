import os
import time
import numpy as np
import pandas as pd
import googlemaps
from dotenv import load_dotenv

load_dotenv()

class DistanceMatrixAPI:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.cache = {}  # Cache for distance matrix results
    
    def get_cache_key(self, origins, destinations):
        """Create a unique key for caching."""
        # Sort to ensure consistent key regardless of order
        orig_key = "|".join(sorted([f"{o['lat']},{o['lng']}" for o in origins]))
        dest_key = "|".join(sorted([f"{d['lat']},{d['lng']}" for d in destinations]))
        return f"{orig_key}:{dest_key}"
    
    def calculate_distance_matrix(self, locations, use_cache=True):
        """Calculate distance matrix for a list of location objects."""
        n = len(locations)
        distance_matrix = np.zeros((n, n))
        duration_matrix = np.zeros((n, n))
        
        # Loop through all pairs of locations
        for i in range(n):
            for j in range(i+1, n):  # Only calculate upper triangle (matrix is symmetric)
                if i == j:
                    continue  # Skip diagonal (distance from point to itself)
                
                origin = [{'lat': locations.iloc[i]['lat'], 'lng': locations.iloc[i]['lng']}]
                destination = [{'lat': locations.iloc[j]['lat'], 'lng': locations.iloc[j]['lng']}]
                
                # Check cache
                cache_key = self.get_cache_key(origin, destination)
                if use_cache and cache_key in self.cache:
                    result = self.cache[cache_key]
                else:
                    try:
                        # Get distance matrix from Google Maps API
                        result = self.gmaps.distance_matrix(
                            origins=origin,
                            destinations=destination,
                            mode="driving",
                            units="metric"
                        )
                        
                        # Cache the result
                        if use_cache:
                            self.cache[cache_key] = result
                        
                        # Respect API rate limits
                        time.sleep(0.2)  # 200ms delay
                    except Exception as e:
                        print(f"Error fetching distance matrix: {str(e)}")
                        # Fallback to straight-line distance if API fails
                        distance_matrix[i, j] = self._calculate_haversine(
                            locations.iloc[i]['lat'], locations.iloc[i]['lng'],
                            locations.iloc[j]['lat'], locations.iloc[j]['lng']
                        ) * 1000  # Convert km to meters
                        duration_matrix[i, j] = distance_matrix[i, j] / 10  # Rough estimate: 10 m/s
                        distance_matrix[j, i] = distance_matrix[i, j]  # Mirror across diagonal
                        duration_matrix[j, i] = duration_matrix[i, j]
                        continue
                
                # Extract distance and duration from result
                if result['status'] == 'OK' and result['rows'][0]['elements'][0]['status'] == 'OK':
                    element = result['rows'][0]['elements'][0]
                    distance = element['distance']['value']  # Distance in meters
                    duration = element['duration']['value']  # Duration in seconds
                    
                    # Fill both upper and lower triangles (symmetric matrix)
                    distance_matrix[i, j] = distance
                    distance_matrix[j, i] = distance
                    duration_matrix[i, j] = duration
                    duration_matrix[j, i] = duration
                else:
                    # Fallback to straight-line distance if API returns error
                    distance_matrix[i, j] = self._calculate_haversine(
                        locations.iloc[i]['lat'], locations.iloc[i]['lng'],
                        locations.iloc[j]['lat'], locations.iloc[j]['lng']
                    ) * 1000  # Convert km to meters
                    duration_matrix[i, j] = distance_matrix[i, j] / 10  # Rough estimate: 10 m/s
                    distance_matrix[j, i] = distance_matrix[i, j]  # Mirror across diagonal
                    duration_matrix[j, i] = duration_matrix[i, j]
        
        return distance_matrix, duration_matrix
    
    def _calculate_haversine(self, lat1, lon1, lat2, lon2):
        """Calculate the great circle distance between two points on earth (specified in decimal degrees)"""
        # Convert decimal degrees to radians
        lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
        c = 2 * np.arcsin(np.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        return c * r
    
    def get_distance_duration_dataframes(self, locations):
        """Return distance and duration matrices as Pandas DataFrames with location labels."""
        dist_matrix, time_matrix = self.calculate_distance_matrix(locations)
        
        # Create DataFrames with location labels
        addresses = locations['address'].tolist()
        dist_df = pd.DataFrame(dist_matrix, index=addresses, columns=addresses)
        time_df = pd.DataFrame(time_matrix, index=addresses, columns=addresses)
        
        return dist_df, time_df 