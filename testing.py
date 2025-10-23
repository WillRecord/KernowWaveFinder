import requests
import pandas as pd

# << ------------------ Build out params for our API call
# Coordinates for Porthleven
LAT = 50.06267
LON = -5.30733

# Marine API - gets the Waves
test_params = {
    "latitude": LAT,
    "longitude": LON,
    "current": ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
    "wind_speed_unit": "mph",
}

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "current": ["wind_speed_10m", "wind_direction_10m", "wind_gusts_10m"],
    "wind_speed_unit": "mph",
}

# Pass the API URL to the get function
response = requests.get("https://api.open-meteo.com/v1/forecast", params=test_params)
print(f"API response code: {response.status_code}")

response_data = response.json()  # Use the pandas built in functionality to hopefully make sense of the JSON


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
