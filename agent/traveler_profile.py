# agent/traveler_profile.py

PROFILES = {
    "solo": {
        "activity_weight": 0.40, # Solos care more about doing things
        "eco_weight": 0.10
    },
    "family": {
        "activity_weight": 0.20, # Families often care more about budget/comfort (implied)
        "eco_weight": 0.20
    },
    "luxury": {
        "activity_weight": 0.20,
        "eco_weight": 0.05
    },
    "default": {
        "activity_weight": 0.30,
        "eco_weight": 0.10
    }
}

def get_profile_weights(profile):
    return PROFILES.get(profile, PROFILES["default"])