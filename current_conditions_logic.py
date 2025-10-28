import pandas as pd

# Need to take the current wave data dictionary and parse it to rate and order spots

# To do this we need to house some information about optimal conditions for spots including;
#  - Optimal swell direction
#  - Optimal wind direction
#  - Optimal Tide
#  - Optimal Swell size/Power

# Need to first take in the different DataFrames and move them into one DF ->
#  At this point probably COULD put into a Database and then query this

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


def is_wave_power_in_sweetspot(wave_height, wave_period):
    power = self.wave_power(wave_height, wave_period)
    if power > self.max_power or power < self.min_power:
        return False
    else:
        return True
