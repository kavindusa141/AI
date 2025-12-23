import random

WEATHER_BY_REGION = {
    "south": "dry",     # Galle, Mirissa
    "north": "hot",     # Jaffna
    "central": "cool",  # Kandy
    "hill": "cool",     # <--- ADDED THIS (Nuwara Eliya, Ella)
    "east": "dry",      # Trincomalee
    "west": "moderate", # Colombo
    "mixed": "moderate"
}

def get_weather(region):
    """
    Simple weather abstraction.
    Returns: 'dry', 'cool', 'hot', 'moderate'
    """
    # Normalize input (handle "Hill", "HILL", "hill ")
    clean_region = str(region).strip().lower()
    
    # Get specific weather or fallback to random
    return WEATHER_BY_REGION.get(clean_region, random.choice(["dry", "cool", "moderate"]))