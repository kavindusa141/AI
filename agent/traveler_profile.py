# agent/traveler_profile.py

PROFILES = {
    "solo": {
        "activity_weight": 0.35,
        "eco_weight": 0.1
    },
    "family": {
        "activity_weight": 0.25,
        "eco_weight": 0.2
    },
    "luxury": {
        "activity_weight": 0.2,
        "eco_weight": 0.05
    },
    "default": {
        "activity_weight": 0.3,
        "eco_weight": 0.1
    }
}


def get_profile_weights(profile):
    return PROFILES.get(profile, PROFILES["default"])
