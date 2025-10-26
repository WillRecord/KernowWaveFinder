import requests
import pandas as pd
from datetime import datetime, timezone

########### Python 3.2 #############

# try:
#     url = "https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations?name=Perranporth"
#
#     headers = {
#         'Cache-Control': 'no-cache',
#         'Ocp-Apim-Subscription-Key': '48b133a1515444799475705e526a4e34',
#     }
#
#     response = requests.get(url, headers=headers)
#
#     # Print status code
#     print(response.status_code)
#
#     # Print response JSON
#     print(response.json())
#
# except Exception as e:
#     print(e)


# 0546A
import requests
from datetime import datetime
import math

try:
    url = "https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/0546A/TidalEvents?duration=1"
    headers = {
        'Cache-Control': 'no-cache',
        'Ocp-Apim-Subscription-Key': '48b133a1515444799475705e526a4e34',
    }

    response = requests.get(url, headers=headers)
    print("Status code:", response.status_code)

    resp_data = response.json()
    now = datetime.now()
    print(f"Current time: {now}\n")

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
        print(f"Previous tide: {prev_tide['height']} ({prev_tide['type']}) at {prev_tide['time']}")
        print(f"Next tide: {next_tide['height']} ({next_tide['type']}) at {next_tide['time']}")

        # Sinusoidal interpolation
        time_elapsed = (now - prev_tide['time']).total_seconds()
        total_tide_time = (next_tide['time'] - prev_tide['time']).total_seconds()
        height_diff = next_tide['height'] - prev_tide['height']

        current_height = prev_tide['height'] + (height_diff / 2) * (1 - math.cos(math.pi * time_elapsed / total_tide_time))
        print(f"Estimated current tide height: {current_height:.2f}")
    else:
        print("Could not determine previous or next tide.")

except Exception as e:
    print("Error:", e)
