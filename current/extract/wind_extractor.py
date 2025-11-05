import requests
import logging


def build_current_wind_params(lat_val, long_val):
    """Uses latitude and longitude as parameters to build a dictionary of parameters needed to query the API"""
    wind_params = {
        "latitude": lat_val,
        "longitude": long_val,
        "current": ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "wind_speed_unit": "mph",
    }
    return wind_params


def extract_current_wind_data(some_params):
    logging.info("Extracting current wind data.")
    # # Pass the API URL to the get function
    wind_response = requests.get("https://api.open-meteo.com/v1/forecast", params=some_params)
    logging.info(f"Current Swell API response code: {wind_response.status_code}")
    return wind_response
