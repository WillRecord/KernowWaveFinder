import logging
import pandas as pd


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