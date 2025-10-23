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


def build_params(spot_name):
    lat_val = SURF_SPOT_LOCATIONS[spot_name]['latitude']
    long_val = SURF_SPOT_LOCATIONS[spot_name]['longitude']
    these_params = {
        "latitude": lat_val,
        "longitude": long_val,
        "current": ["swell_wave_height", "swell_wave_direction", "swell_wave_period", "wind_wave_period",
                    "sea_surface_temperature", "sea_level_height_msl"]
    }
    return these_params


def extract(some_params):
    print(f"...Extracting..")
    # Pass the API URL to the get function
    response = requests.get('https://marine-api.open-meteo.com/v1/marine', params=some_params)
    print(f"API response code: {response.status_code}")
    return response


def transform(response_obj, spot):
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
params = build_params(spot_name)
response = extract(params)
df_result = transform(response, spot_name)
