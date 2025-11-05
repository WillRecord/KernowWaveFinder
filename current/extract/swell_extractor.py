import requests
import logging


def build_current_swell_params(lat_val, long_val):
    """Uses latitude and longitude as parameters to build a dictionary of parameters needed to query the API"""
    swell_params = {
        "latitude": lat_val,
        "longitude": long_val,
        "current": ["swell_wave_height", "swell_wave_direction", "swell_wave_period", "wind_wave_period",
                    "sea_surface_temperature", "sea_level_height_msl"]
    }
    return swell_params


def extract_current_swell_data(some_params):
    logging.info("Extracting current swell data.")
    # Pass the API URL to the get function
    swell_response = requests.get('https://marine-api.open-meteo.com/v1/marine', params=some_params)
    logging.info(f"Current Swell API response code: {swell_response.status_code}")
    return swell_response
