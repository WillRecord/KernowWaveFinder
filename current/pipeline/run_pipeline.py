import pandas as pd
from current.constants import SURF_SPOT_LOCATIONS
import logging
# Import Extract Functionality
from current.extract.tide_extractor import build_curr_tide_params, extract_current_tide_data
from current.extract.wind_extractor import build_current_wind_params, extract_current_wind_data
from current.extract.swell_extractor import build_current_swell_params, extract_current_swell_data
# Import Transform Functionality
from current.transform.swell_transformer import transform_curr_swell_response
from current.transform.tide_transformer import transform_curr_tide_response
from current.transform.wind_transformer import transform_curr_wind_response
from current.rating_logic import rate_curr_spot


logger = logging.getLogger(__name__)


def build_curr_api_params(spot_name):
    """Builds out parameters for all our API calls using the spotname to query the dictionary and then returning the
    params in a tuple"""
    logging.info("... << ---- Building API Parameters and Headers --- >> ...")
    # Get LATITUDE and LONGITUDE spot values from dictionary to use in params
    lat = SURF_SPOT_LOCATIONS[spot_name]['latitude']
    long = SURF_SPOT_LOCATIONS[spot_name]['longitude']
    swell_params = build_current_swell_params(lat, long)  # << ------------ Get the swell params
    wind_params = build_current_wind_params(lat, long)  # << ------------ Get the wind params
    tide_params = build_curr_tide_params(spot_name)  # << ------------ Get the tide params
    return swell_params, wind_params, tide_params


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


# spot_name = 'Perranporth'
# params_tup = build_curr_api_params(spot_name)
# response_tuple = extract_current_data(params_tup)
# df_result = transform_curr_api_responses(response_tuple, spot_name)
# print(df_result.to_dict(orient='records'))
# print(df_result.columns)

# spot = "Perranporth"
# params = build_curr_api_params(spot)
# responses = extract_current_data(params)
# df = transform_curr_api_responses(responses, spot)
# rating = rate_all_spots(SURF_SPOT_LOCATIONS[spot], df.iloc[0])
# print(f"{spot} Surf Rating: {rating['rating']}/10 ({rating['wind_dir_str']} wind)")


def rate_all_spots():
    results = []

    logging.info("Starting rate_all_spots() pipeline...")

    for spot_name in SURF_SPOT_LOCATIONS.keys():
        logging.info(f"Processing spot: {spot_name}")

        params = build_curr_api_params(spot_name)
        responses = extract_current_data(params)
        df_row = transform_curr_api_responses(responses, spot_name).iloc[0]

        logging.info(f"Transformed DataFrame row for {spot_name}: {df_row.to_dict()}")

        rating_results = rate_curr_spot(SURF_SPOT_LOCATIONS[spot_name], df_row)

        logging.info(
            f"{spot_name}: rating={rating_results['rating']} wind_dir={rating_results['wind_dir_str']}"
        )

        # Produce correct flat dict
        results.append({
            "spot_name": spot_name,
            "rating": rating_results["rating"],
            "wind_direction": rating_results["wind_dir_str"],
            # Add more if they exist:
            # "swell_height": df_row.get("swell_height"),
            # "tide_state": df_row.get("tide_state"),
        })

    logging.info("Completed rate_all_spots()")
    return results

