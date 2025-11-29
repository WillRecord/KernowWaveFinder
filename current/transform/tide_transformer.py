import logging
from datetime import datetime
import math

import pandas as pd


def parse_iso_flexible(ts: str) -> datetime:
    # If the timestamp has fractional seconds
    if '.' in ts:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f")
    # No fractional seconds
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S")


def transform_curr_tide_response(resp, spot):
    resp_data = resp.json()
    resp_data.sort(key=lambda t: parse_iso_flexible(t["DateTime"]))  # Check that the tides are in order

    now = datetime.now()
    logging.debug(f"Current time now is: {now}")

    prev_tide = None
    next_tide = None

    # Loop through all tides to find prev and next
    for tide in resp_data:
        tide_time = parse_iso_flexible(tide['DateTime'])  # Fix for bug with invalid iso formats
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