import math


def calculate_absolute_humidity(relative_humidity, temperature, atmospheric_pressure):
    """
    Calculates the absolute humidity of air.

    Args:
        relative_humidity (float): Relative humidity as a percentage.
        temperature (float): Temperature in degrees Celsius.
        atmospheric_pressure (float): Atmospheric pressure in kpa.

    Returns:
        float: Absolute humidity in grams per cubic meter.
    """
    ah = []
    for rh, t, ap in zip(relative_humidity,temperature, atmospheric_pressure):

        # Saturation Vapor Pressure (SVP) calculation
        svp = 6.11 * math.exp((17.502 * t) / (t + 240.97))

        # Vapor Pressure (VP) calculation
        vp = (rh / 100) * svp

        # Absolute Humidity calculation
        absolute_humidity = (216.7 * vp) / (273.15 + t)
        absolute_humidity *= 100 / ap  # Convert to grams per cubic meter
        ah.append(absolute_humidity)
    return ah


