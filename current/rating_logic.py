import pandas as pd
from current.constants import SURF_SPOT_LOCATIONS
from current.pipeline.run_etl import build_curr_api_params, extract_current_data, transform_curr_api_responses

# Test Data
example_test_data = {'wave_height': 0.7, 'wave_height_unit': 'm',
                     'wave_direction': 215, 'wave_direction_unit': '°',
                     'wave_period': 6.65, 'wave_period_unit': 's',
                     'water_temperature': 13.6, 'water_temperature_unit': '°C',
                     'wind_speed': 19.0, 'wind_speed_unit': 'mp/h',
                     'wind_direction': 277, 'wind_direction_unit': '°',
                     'wind_gusts': 31.1, 'wind_gusts_unit': 'mp/h',
                     'Curr_tide_height': 5.669016004113615}

example_test_df = pd.DataFrame(example_test_data, index=[0])


# << ================================ HELPER FUNCTIONS ================================ >>

def wind_relative_to_spot(spot, wind_dir, wind_mph, debug=True):
    """Gives the wind a rating from 0 to 5 and returns label for direction e,g, offshore as a string"""
    wind_score = 0  # Variable to track the wind score
    # Angle between current wind and optimal direction for offshore
    wind_diff = abs((wind_dir - spot['optimal_wind_dir'] + 180) % 360 - 180)
    # Verbose mode: print debug info
    if debug:
        print(f"Spot row: {spot}")
        print(f"Optimal wind dir: {spot['optimal_wind_dir']}°")
        print(f"Current wind dir: {wind_dir}°")
        print(f"Difference: {wind_diff:.1f}°")
    # Determine scoring and category
    if wind_diff <= 45:
        direction = "Offshore"
        wind_score = 5
        if wind_mph > 40:  # Adjust for strong off-shores
            wind_score -= 1
        elif wind_mph > 20:  # Adjust for strong off-shores
            wind_score -= 0.5
    elif wind_diff <= 90:
        direction = "Cross-off"
        wind_score = 3
        if wind_mph > 40:  # Adjust for strong off-shores
            wind_score -= 1
        elif wind_mph > 20:  # Adjust for strong off-shores
            wind_score -= 0.5
    else:
        direction = "Onshore"
        wind_score = 1
        if wind_mph > 20:  # Adjust for strong crap conditions
            wind_score -= 1
        elif wind_mph > 15:  # Adjust for strong on-shores
            wind_score -= 0.5

    if debug:
        print(f"Wind is: {wind_mph}mph {direction} scoring given is {wind_score}/5\n")

    return direction, wind_score

def wave_period_rating(wave_period):
    """Rates wave period from 1-5"""
    if wave_period < 6:
        period_rating = 1  # short-period wind swell
    elif wave_period < 8:
        period_rating = 2
    elif wave_period < 10:
        period_rating = 3
    elif wave_period < 12:
        period_rating = 4
    else:
        period_rating = 5  # long-period ground swell
    print(f"Wave period is {wave_period}, given rating of {period_rating}/5")
    return period_rating


def wave_height_rating(height):
    """Provides a cap for how good the score can be based on the wave size"""
    if height < 1:
        size_cap = 2  # almost flat
    elif height < 3:
        size_cap = 7  # small fun waves
    elif height < 4:
        size_cap = 9  # getting solid size
    else:
        size_cap = 10  # solid/scary
    return size_cap


def tide_penalty(spot, tide):
    """If tide is too high or too low provides a penalty to then be applied to the score"""
    if tide < spot['tidal_range_low'] or tide > spot['tidal_range_high']:
        tide_penalty = -1.5  # tide too high or too low hurts quality
    else:
        tide_penalty = 0  # within working range

    return tide_penalty


def rate_curr_spot(spot, row):
    """Logic to rate spots current conditions"""
    # << ------------------- Get Factors from helper functions
    wind_dir, wind_score = wind_relative_to_spot(spot, row['wind_direction'], row['wind_speed'])  # 1. Wind dir score
    period_score = wave_period_rating(row['wave_period'])                                       # 2. Wave period score
    size_cap = wave_height_rating(row['wave_height'])                                           # 3. Wave height score
    tide_adj = tide_penalty(spot, row['Curr_tide_height'])                                  # 4. Tide adjustment factor

    # Algorithm to rate is a Weighted combination of the above factors (wind_score is 50% whilst period is 30%)
    raw_score = (wind_score * 0.5) + (period_score * 0.3) + 2
    adjusted_score = raw_score + tide_adj                                                     # Then we adjust for tide
    final_score = max(0, min(size_cap, adjusted_score))                # The score is finally capped by the wave height
    final_score = round(final_score, 1)  # We then round to 1 decimal place

    # Combine output into a dictionary
    spot_rating_dict = {'rating': final_score,
                        'wind_dir_str': wind_dir
                        # 'notes':
                        }

    return spot_rating_dict


# spot_info = SURF_SPOT_LOCATIONS['Perranporth']
# spot_score_dict = rate_curr_spot(spot_info, example_test_df.iloc[0])
# print(f"Perranporth Surf Rating: {spot_score_dict['rating']}/10 and {spot_score_dict['wind_dir_str']} wind.")   # TEST RUN
# Loop through the spots and call the et part of the etl for each including the rating logic
# After each loop
def rate_all_spots(spot, row):
    results_listofdict = []
    for spot_name in SURF_SPOT_LOCATIONS.keys():
        params = build_curr_api_params(spot_name)
        responses = extract_current_data(params)
        df = transform_curr_api_responses(responses, spot_name)
        print(f"Spot name is {SURF_SPOT_LOCATIONS[spot_name]}")
        print(f"Second param is our Dataframe: \n{df}")
        # Perform same rating logic above and add to
        this_rating = rate_curr_spot(SURF_SPOT_LOCATIONS[spot_name], df)
        print(f"{spot_name} Surf Rating: {this_rating['rating']}/10 ({this_rating['wind_dir_str']} wind)")
        # Add our result to a dictionary?
        results_listofdict.append({spot_name: this_rating})

    print(f"FINAL RESULT:\n{results_listofdict}")


# <<< UNFINISHED LOGIC AROUND POWER SWEETSPOT
# def wave_power(wave_height, wave_period):
#     # Rough wave power per meter of wave front (KJ/m)
#     rho = 1025  # kg/m³
#     g = 9.81  # m/s²
#     power = (rho * g ** 2 / (64 * 3.1416)) * wave_height ** 2 * wave_period
#     return power
#
#
# def is_wave_power_in_sweetspot(df):
#     power = wave_power(df['wave_height'], df['wave_direction'])
#     if power > df['max_power'] or power < df['']:
#         return False
#     else:
#         return True
