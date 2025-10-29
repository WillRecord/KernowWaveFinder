import pandas as pd

SURF_SPOT_LOCATIONS = {
    "Perranporth": {"latitude": 50.4165, "longitude": -5.071, 'tide_key': '0546A',
                    'optimal_wind_dir': 290, 'optimal_swell_dir': 110, 'swell_range_low': 50,
                    'swell_range_high': 500, 'tidal_range_low': 0, 'tidal_range_high': 7},
    "Porthleven": {"latitude": 50.06267, "longitude": -5.30733, 'tide_key': 'X',
                   'optimal_wind_dir': 220, 'optimal_swell_dir': 40, 'swell_range': '50-1000',
                   'tidal_range_low': 1, 'tidal_range_high': 5},
    "Praa Sands": {"latitude": 50.1019, "longitude": -5.3945, 'tide_key': 'X',
                   'optimal_wind_dir': 220, 'optimal_swell_dir': 40, 'swell_range': '100-700',
                   'tidal_range_low': 0, 'tidal_range_high': 4.5},
    "Porthmeor": {"latitude": 50.2160, "longitude": -5.5363, 'tide_key': 'X',
                  'optimal_wind_dir': 290, 'optimal_swell_dir': 110, 'swell_range': '400-2000',
                  'tidal_range_low': 0, 'tidal_range_high': 4},
    "Swanpool": {"latitude": 50.1415, "longitude": -5.0712, 'tide_key': 'X',
                 'optimal_wind_dir': 140, 'optimal_swell_dir': 320, 'swell_range': '50-10000',
                 'tidal_range_low': 1, 'tidal_range_high': 3.5}
}


# To do this we need to house some information about optimal conditions for spots including;
#  - Optimal swell direction ✅
#  - Optimal wind direction ✅
#  - Optimal Tidal range ✅
#  - Optimal Swell size/Power ✅

# Reference index of dataframe columns
# 'wave_height', 'wave_height_unit', 'wave_direction',
#        'wave_direction_unit', 'wave_period', 'wave_period_unit',
#        'water_temperature', 'water_temperature_unit', 'wind_speed',
#        'wind_speed_unit', 'wind_direction', 'wind_direction_unit',
#        'wind_gusts', 'wind_gusts_unit', 'Curr_tide_height'

def rate_curr_spot(spot_df):
    # Need to take the current wave DataFrame and parse it to rate and order spots
    pass


def wind_relative_to_spot(spot, wind_dir):
    relative_wind_dir = ((wind_dir - spot['orientation']) + 360) % 360
    if relative_wind_dir > 315 or relative_wind_dir < 45:
        return "Offshore"
    elif (45 < relative_wind_dir < 135) or (225 < relative_wind_dir < 315):
        return "Cross-off"
    else:
        return "Onshore"


def wave_power(wave_height, wave_period):
    # Rough wave power per meter of wave front (KJ/m)
    rho = 1025  # kg/m³
    g = 9.81  # m/s²
    power = (rho * g ** 2 / (64 * 3.1416)) * wave_height ** 2 * wave_period
    return power


def is_wave_power_in_sweetspot(df):
    power = wave_power(df['wave_height'], df['wave_direction'])
    if power > df['max_power'] or power < df['']:
        return False
    else:
        return True

def rate_curr_conditions(df):
    # If the direction of the swell is outside the range -> 0 stars as wave won't break
    # If the direction of the wind is offshore
    pass
