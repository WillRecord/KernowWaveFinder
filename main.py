import requests
import pandas as pd

# << ------------------ Build out params for our API call
# Coordinates for spots
SURF_SPOT_LOCATIONS = {
    "Perranporth": {"latitude": 50.4165, "longitude": -5.071},
    "Porthleven": {"latitude": 50.06267, "longitude": -5.30733},
    "Praa Sands": {"latitude": 50.1019, "longitude": -5.3945},
    "Porthmeor": {"latitude": 50.2160, "longitude": -5.5363},
    "Swanpool": {"latitude": 50.1415, "longitude": -5.0712}
}


def convert_msl_to_cd(spot_name, tide_val):
    print(f'Converting tide height MSL: {tide_val}')
    msl_cd_offset = {'Perranporth': 2.2,
                     "Porthleven": 2.3,
                     "Praa Sands": 2.3,
                     "Porthmeor": 2.2,
                     'Swanpool': 2.1}
    offset = msl_cd_offset[spot_name]
    print(f'CD: {tide_val + offset}')
    return tide_val + offset


def build_curr_api_params(spot_name):
    """Builds out parameters for all our API calls using the spotname to query the dictionary and then returning the
    params in a tuple"""
    # Get LATITUDE and LONGITUDE spot values from dictionary to use in params
    lat = SURF_SPOT_LOCATIONS[spot_name]['latitude']
    long = SURF_SPOT_LOCATIONS[spot_name]['longitude']
    swell_params = build_current_swell_params(lat, long)  # << ------------ Get the swell params
    wind_params = build_current_wind_params(lat, long)  # << -------------- Get the wind params
    return swell_params, wind_params


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
    """Takes a tuple of params and queries the APIs via separate functions for wind and swell.
    Returns the response objects as a tuple."""
    swell_params, wind_params = params_tuple  # Unpack Tuple
    swell_response_obj = extract_current_swell_data(swell_params)
    wind_response_obj = extract_current_wind_data(wind_params)
    return swell_response_obj, wind_response_obj


def extract_current_swell_data(some_params):
    print(f"...Extracting current swell data..")
    # Pass the API URL to the get function
    swell_response = requests.get('https://marine-api.open-meteo.com/v1/marine', params=some_params)
    print(f"Current Swell API response code: {swell_response.status_code}")
    return swell_response


def extract_current_wind_data(some_params):
    print(f"...Extracting current wind data..")
    # # Pass the API URL to the get function
    wind_response = requests.get("https://api.open-meteo.com/v1/forecast", params=some_params)
    print(f"Current Wind API response code: {wind_response.status_code}")
    return wind_response


def transform_curr_api_responses(Curr_api_resp_tuple, spot):
    print(f"...TRANSFORMING API RESPONSES...")
    swell_resp, wind_resp = Curr_api_resp_tuple  # Unpack Tuple
    swell_df = transform_curr_swell_response(swell_resp, spot)
    wind_df = transform_curr_wind_response(wind_resp, spot)
    print(f"Got to the end!")
    return swell_df, wind_df


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
    print(combined_data)
    combined_df = pd.DataFrame(data=combined_data, index=[0])
    print(combined_df)
    return combined_df


def transform_curr_swell_response(response_obj, spot):
    print(f"...Transforming..")
    response_data = response_obj.json()  # Use the pandas built in functionality to hopefully make sense of the JSON
    wave_data = response_data['current']
    unit_data = response_data['current_units']
    # Convert tide heights from msl to cd
    msl = wave_data['sea_level_height_msl']
    cd = convert_msl_to_cd(spot, msl)
    combined_data = {
        "wave_height": wave_data['swell_wave_height'],
        "wave_height_unit": unit_data['swell_wave_height'],
        "wave_direction": wave_data['swell_wave_direction'],
        "wave_direction_unit": unit_data['swell_wave_direction'],
        "wave_period": wave_data['swell_wave_period'],
        "wave_period_unit": unit_data['swell_wave_period'],
        "water_temperature": wave_data['sea_surface_temperature'],
        "water_temperature_unit": unit_data['sea_surface_temperature'],
        "tide_height": cd,
        "tide_height_unit": unit_data['sea_level_height_msl']
    }
    print(combined_data)
    combined_df = pd.DataFrame(data=combined_data, index=[0])
    return combined_df


spot_name = 'Perranporth'
params_tup = build_curr_api_params(spot_name)
response_tuple = extract_current_data(params_tup)
df_result = transform_curr_api_responses(response_tuple, spot_name)
