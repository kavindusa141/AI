# environment/weather.py

import random

WEATHER_BY_REGION = {
    "south": "dry",
    "north": "hot",
    "central": "cool",
    "east": "dry",
    "mixed": "moderate"
}


def get_weather(region):
    """
    Simple weather abstraction.
    Can be replaced with real API later.
    """
    return WEATHER_BY_REGION.get(region, random.choice(["dry", "cool", "moderate"]))
