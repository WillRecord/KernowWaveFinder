from current.constants import SURF_SPOT_LOCATIONS, API_KEY
import requests
import logging


def build_curr_tide_params(spot):
    id = SURF_SPOT_LOCATIONS[spot]['tide_key']
    return id


def extract_current_tide_data(spot_id):
    logging.info("Extracting current tide data.")
    try:
        url = "https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0546A/TidalEvents?duration=1"
        headers = {
            'Cache-Control': 'no-cache',
            'Ocp-Apim-Subscription-Key': API_KEY,
        }
        response = requests.get(url, headers=headers)
        logging.info(f"Current Tide API response code: {response.status_code}")
        return response
    except Exception as e:
        print("Error:", e)

