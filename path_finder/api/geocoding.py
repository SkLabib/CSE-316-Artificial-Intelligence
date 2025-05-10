import os
import time
import googlemaps
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

class GeocodingAPI:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.gmaps = googlemaps.Client(key=self.api_key)
        self.cache = {}  # Simple cache to avoid redundant API calls
    
    def geocode_address(self, address):
        """Convert a single address to latitude/longitude coordinates."""
        # Check cache first
        if address in self.cache:
            return self.cache[address]
        
        try:
            # Make API call with error handling and rate limiting
            geocode_result = self.gmaps.geocode(address)
            
            if geocode_result and len(geocode_result) > 0:
                location = geocode_result[0]['geometry']['location']
                result = {
                    'address': address,
                    'lat': location['lat'],
                    'lng': location['lng'],
                    'formatted_address': geocode_result[0]['formatted_address']
                }
                # Cache the result
                self.cache[address] = result
                return result
            else:
                print(f"Warning: Could not geocode address: {address}")
                return None
        except Exception as e:
            print(f"Error geocoding address '{address}': {str(e)}")
            # Return default fallback
            return None
        finally:
            # Rate limiting to respect Google's API limits
            time.sleep(0.2)  # 200ms delay between requests
    
    def batch_geocode(self, addresses):
        """Convert multiple addresses to coordinates."""
        results = []
        
        for address in addresses:
            result = self.geocode_address(address)
            if result:
                results.append(result)
        
        return pd.DataFrame(results)
    
    def geocode_from_csv(self, csv_file, address_column="address"):
        """Read addresses from CSV and convert to coordinates."""
        try:
            df = pd.read_csv(csv_file)
            addresses = df[address_column].tolist()
            return self.batch_geocode(addresses)
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
            return pd.DataFrame() 