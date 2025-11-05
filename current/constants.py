from dotenv import load_dotenv
import os

# Coordinates for spots
SURF_SPOT_LOCATIONS = {
    "Perranporth": {
        "latitude": 50.4165,
        "longitude": -5.071,
        'tide_key': '0546A',
        'optimal_wind_dir': 110,
        'optimal_swell_dir': 290,
        'swell_range_low': 50,
        'swell_range_high': 500,
        'tidal_range_low': 0,
        'tidal_range_high': 7
    },
    "Porthleven": {
        "latitude": 50.06267,
        "longitude": -5.30733,
        'tide_key': '0002A',
        'optimal_wind_dir': 40,
        'optimal_swell_dir': 220,
        'swell_range': '50-1000',
        'tidal_range_low': 1,
        'tidal_range_high': 5
    },
    "Praa Sands": {
        "latitude": 50.1019,
        "longitude": -5.3945,
        'tide_key': '0002',
        'optimal_wind_dir': 40,
        'optimal_swell_dir': 220,
        'swell_range': '100-700',
        'tidal_range_low': 0,
        'tidal_range_high': 4.5
    },
    "Porthmeor": {
        "latitude": 50.2160,
        "longitude": -5.5363,
        'tide_key': '0547',
        'optimal_wind_dir': 110,
        'optimal_swell_dir': 290,
        'swell_range': '400-2000',
        'tidal_range_low': 0,
        'tidal_range_high': 4
    },
    "Swanpool": {
        "latitude": 50.1415,
        "longitude": -5.0712,
        'tide_key': '0005',
        'optimal_wind_dir': 320,
        'optimal_swell_dir': 140,
        'swell_range': '50-10000',
        'tidal_range_low': 1,
        'tidal_range_high': 3.5
    }
}

load_dotenv()   # reads .env
API_KEY = os.getenv("SUPER_SECRET_API_KEY")
