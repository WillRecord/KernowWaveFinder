import pandas as pd


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
