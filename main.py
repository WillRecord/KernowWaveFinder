import os
import requests
from datetime import datetime
import math
from dotenv import load_dotenv
import logging
from current.current_conditions_logic import *

# << ------------------ Build out params for our API call
# Coordinates for spots
SURF_SPOT_LOCATIONS = {
    "Perranporth": {"latitude": 50.4165, "longitude": -5.071, 'tide_key': '0546A',
                    'optimal_wind_dir': 110, 'optimal_swell_dir': 290,
                    'swell_range_low': 50, 'swell_range_high': 500,
                    'tidal_range_low': 0, 'tidal_range_high': 7},
    "Porthleven": {"latitude": 50.06267, "longitude": -5.30733, 'tide_key': 'X',
                   'optimal_wind_dir': 40, 'optimal_swell_dir': 220,
                   'swell_range': '50-1000',
                   'tidal_range_low': 1, 'tidal_range_high': 5},
    "Praa Sands": {"latitude": 50.1019, "longitude": -5.3945, 'tide_key': 'X',
                   'optimal_wind_dir': 40, 'optimal_swell_dir': 220,
                   'swell_range': '100-700',
                   'tidal_range_low': 0, 'tidal_range_high': 4.5},
    "Porthmeor": {"latitude": 50.2160, "longitude": -5.5363, 'tide_key': 'X',
                  'optimal_wind_dir': 110, 'optimal_swell_dir': 290,
                  'swell_range': '400-2000',
                  'tidal_range_low': 0, 'tidal_range_high': 4},
    "Swanpool": {"latitude": 50.1415, "longitude": -5.0712, 'tide_key': 'X',
                 'optimal_wind_dir': 320, 'optimal_swell_dir': 140,
                 'swell_range': '50-10000',
                 'tidal_range_low': 1, 'tidal_range_high': 3.5}
}

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)


load_dotenv()   # reads .env
api_key = os.getenv("SUPER_SECRET_API_KEY")


def build_curr_api_params(spot_name):
    """Builds out parameters for all our API calls using the spotname to query the dictionary and then returning the
    params in a tuple"""
    logging.info("... << ---- Building API Parameters and Headers --- >> ...")
    # Get LATITUDE and LONGITUDE spot values from dictionary to use in params
    lat = SURF_SPOT_LOCATIONS[spot_name]['latitude']
    long = SURF_SPOT_LOCATIONS[spot_name]['longitude']
    swell_params = build_current_swell_params(lat, long)  # << ------------ Get the swell params
    wind_params = build_current_wind_params(lat, long)    # << ------------ Get the wind params
    tide_params = build_curr_tide_params(spot_name)       # << ------------ Get the tide params
    return swell_params, wind_params, tide_params


def build_curr_tide_params(spot):
    id = SURF_SPOT_LOCATIONS[spot]['tide_key']
    return id


def build_current_wind_params(lat_val, long_val):
    """Uses latitude and longitude as parameters to build a dictionary of parameters needed to query the API"""
    wind_params = {
        "latitude": lat_val,
        "longitude": long_val,
        "current": ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
        "wind_speed_unit": "mph",
    }
    return wind_params


def build_current_swell_params(lat_val, long_val):
    """Uses latitude and longitude as parameters to build a dictionary of parameters needed to query the API"""
    swell_params = {
        "latitude": lat_val,
        "longitude": long_val,
        "current": ["swell_wave_height", "swell_wave_direction", "swell_wave_period", "wind_wave_period",
                    "sea_surface_temperature", "sea_level_height_msl"]
    }
    return swell_params


def extract_current_data(params_tuple):
    """Takes a tuple of params and queries the APIs via separate functions for wind, swell and tides.
    Returns the response objects as a tuple."""
    logging.info("... << ---- STARTING EXTRACT ---- >> ...")
    swell_params, wind_params, tide_params = params_tuple  # Unpack Tuple
    swell_response_obj = extract_current_swell_data(swell_params)  # Swell API query
    wind_response_obj = extract_current_wind_data(wind_params)  # Wind API Query
    tide_response_obj = extract_current_tide_data(tide_params)
    logging.info("... << ---- EXTRACT COMPLETE ---- >> ...")
    return swell_response_obj, wind_response_obj, tide_response_obj


def extract_current_tide_data(spot_id):
    logging.info("Extracting current tide data.")
    try:
        url = "https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0546A/TidalEvents?duration=1"
        headers = {
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': api_key,
        }
        response = requests.get(url, headers=headers)
        logging.info(f"Current Tide API response code: {response.status_code}")
        return response
    except Exception as e:
        print("Error:", e)


def extract_current_swell_data(some_params):
    logging.info("Extracting current swell data.")
    # Pass the API URL to the get function
    swell_response = requests.get('https://marine-api.open-meteo.com/v1/marine', params=some_params)
    logging.info(f"Current Swell API response code: {swell_response.status_code}")
    return swell_response


def extract_current_wind_data(some_params):
    logging.info("Extracting current wind data.")
    # # Pass the API URL to the get function
    wind_response = requests.get("https://api.open-meteo.com/v1/forecast", params=some_params)
    logging.info(f"Current Swell API response code: {wind_response.status_code}")
    return wind_response


def transform_curr_api_responses(curr_api_resp_tuple, spot):
    logging.info(f"... << ---- TRANSFORMING API RESPONSES ---- >> ...")
    swell_resp, wind_resp, tide_resp = curr_api_resp_tuple  # Unpack Tuple

    # Get all the DataFrames nicely formatted
    # Swell
    swell_df = transform_curr_swell_response(swell_resp, spot)
    if not isinstance(swell_df, pd.DataFrame):
        logging.error("transform_curr_swell_response() did not return a DataFrame.")
        raise TypeError("transform_curr_swell_response() must return a DataFrame")

    # Wind
    wind_df = transform_curr_wind_response(wind_resp, spot)
    if not isinstance(wind_df, pd.DataFrame):
        logging.error("transform_curr_wind_response() did not return a DataFrame.")
        raise TypeError("transform_curr_wind_response() must return a DataFrame")

    # Tide
    tide_df = transform_curr_tide_response(tide_resp, spot)
    if not isinstance(tide_df, pd.DataFrame):
        logging.error("transform_curr_tide_response() did not return a DataFrame.")
        raise TypeError("transform_curr_tide_response() must return a DataFrame")

    # Combine them all
    combined_df = pd.concat([swell_df, wind_df, tide_df], axis=1)  # Combine all the DataFrames
    logging.info(f"... << ---- TRANSFORM COMPLETE combined df has shape {combined_df.shape} ---- >> ...")
    return combined_df


def transform_curr_tide_response(resp, spot):
    resp_data = resp.json()
    now = datetime.now()
    logging.debug(f"Current time now is: {now}")

    prev_tide = None
    next_tide = None

    # Loop through all tides to find prev and next
    for tide in resp_data:
        tide_time = datetime.fromisoformat(tide['DateTime'])
        if tide_time <= now:
            prev_tide = {
                "type": tide['EventType'],
                "height": tide['Height'],
                "time": tide_time
            }
        elif tide_time > now and next_tide is None:
            next_tide = {
                "type": tide['EventType'],
                "height": tide['Height'],
                "time": tide_time
            }

    if prev_tide and next_tide:
        logging.debug(f"Previous tide: {prev_tide['height']} ({prev_tide['type']}) at {prev_tide['time']}")
        logging.debug(f"Next tide: {next_tide['height']} ({next_tide['type']}) at {next_tide['time']}")

        # Sinusoidal interpolation
        time_elapsed = (now - prev_tide['time']).total_seconds()
        total_tide_time = (next_tide['time'] - prev_tide['time']).total_seconds()
        height_diff = next_tide['height'] - prev_tide['height']

        current_height = prev_tide['height'] + (height_diff / 2) * (
                    1 - math.cos(math.pi * time_elapsed / total_tide_time))
        logging.debug(f"Estimated current tide height: {current_height:.2f}")
        tide_dict = {'Curr_tide_height': current_height}  # Put in a dictionary
        tide_df = pd.DataFrame(tide_dict, index=[0])
        return tide_df
    else:
        logging.debug("Could not determine previous or next tide.")


def transform_curr_wind_response(wind_resp, spot):
    response_data = wind_resp.json()  # Use the pandas built in functionality to hopefully make sense of the JSON
    wind_data = response_data['current']
    wind_units = response_data['current_units']
    combined_data = {
        "wind_speed": wind_data['wind_speed_10m'],
        "wind_speed_unit": wind_units['wind_speed_10m'],
        "wind_direction": wind_data['wind_direction_10m'],
        "wind_direction_unit": wind_units['wind_direction_10m'],
        "wind_gusts": wind_data['wind_gusts_10m'],
        "wind_gusts_unit": wind_units['wind_gusts_10m']
    }
    combined_df = pd.DataFrame(data=combined_data, index=[0])
    return combined_df


def transform_curr_swell_response(response_obj, spot):
    logging.info(f"Transforming swell response")
    response_data = response_obj.json()  # Use the pandas built in functionality to hopefully make sense of the JSON
    wave_data = response_data['current']
    unit_data = response_data['current_units']
    combined_data = {
        "wave_height": wave_data['swell_wave_height'],
        "wave_height_unit": unit_data['swell_wave_height'],
        "wave_direction": wave_data['swell_wave_direction'],
        "wave_direction_unit": unit_data['swell_wave_direction'],
        "wave_period": wave_data['swell_wave_period'],
        "wave_period_unit": unit_data['swell_wave_period'],
        "water_temperature": wave_data['sea_surface_temperature'],
        "water_temperature_unit": unit_data['sea_surface_temperature']
    }
    combined_df = pd.DataFrame(data=combined_data, index=[0])
    return combined_df


# spot_name = 'Perranporth'
# params_tup = build_curr_api_params(spot_name)
# response_tuple = extract_current_data(params_tup)
# df_result = transform_curr_api_responses(response_tuple, spot_name)
# print(df_result.to_dict(orient='records'))
# print(df_result.columns)

# Need to loop through all our
spot = "Perranporth"
params = build_curr_api_params(spot)
responses = extract_current_data(params)
df = transform_curr_api_responses(responses, spot)
rating = rate_curr_spot(SURF_SPOT_LOCATIONS[spot], df.iloc[0])
print(f"{spot} Surf Rating: {rating['rating']}/10 ({rating['wind_dir_str']} wind)")
