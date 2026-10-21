"""
Script to load geographical data into a pandas DataFrame, and save it as a
CSV file.
"""

import numpy as np
import pandas as pd
from geopy.exc import GeopyError
from geopy.geocoders import Nominatim


def get_geolocator(agent="h501-student"):
    """
    Initiate a Nominatim geolocator instance given an `agent`.

    Parameters
    ----------
    agent : str, optional
        Agent name for Nominatim, by default 'h501-student'
    """
    return Nominatim(user_agent=agent)


def empty_location(loc):
    """Return a row with NA values for a location that wasn't found."""
    return {
        "location": loc,
        "latitude": np.nan,
        "longitude": np.nan,
        "type": np.nan,
    }


def fetch_location_data(geolocator, loc):
    """
    Look up one location and return its name, coordinates, and type.

    If the location can't be found (or the lookup fails), the name is
    kept and every other value is NA.
    """
    try:
        location = geolocator.geocode(loc, timeout=10)
    except GeopyError as error:
        print(f"Could not look up {loc!r}: {error}")
        return empty_location(loc)
    if location is None:
        return empty_location(loc)
    return {
        "location": loc,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "type": location.raw.get("type", "").capitalize() or np.nan,
    }


def build_geo_dataframe(locations, geolocator=None):
    """Return a DataFrame with one row of location data per location."""
    if geolocator is None:
        geolocator = get_geolocator()
    geo_data = [fetch_location_data(geolocator, loc) for loc in locations]

    return pd.DataFrame(geo_data)


if __name__ == "__main__":
    geo = get_geolocator()
    locations = [
        "Museum of Modern Art",
        "iuyt8765(*&)",
        "Alaska",
        "Franklin's Barbecue",
        "Burj Khalifa",
    ]
    df = build_geo_dataframe(locations, geo)

    df.to_csv("./geo_data.csv", index=False)
    
