import json
import random

INPUT_FILE = "tour_packages.json"
OUTPUT_FILE = "tour_packages_cleaned.json"

# -------------------------------
# REALISTIC ACTIVITY MAP
# -------------------------------
ACTIVITY_MAP = {
    "Kalpitiya": [
        ("Dolphin & Whale Watching", "adventure"),
        ("Kite Surfing Session", "adventure")
    ],
    "Mirissa": [
        ("Whale Watching Boat Tour", "beach"),
        ("Coconut Tree Hill Sunset", "beach")
    ],
    "Galle": [
        ("Galle Fort Heritage Walk", "culture"),
        ("Maritime Museum Visit", "culture")
    ],
    "Ella": [
        ("Nine Arches Bridge Visit", "nature"),
        ("Little Adam’s Peak Hike", "nature")
    ],
    "Sigiriya": [
        ("Sigiriya Rock Fortress Climb", "heritage"),
        ("Pidurangala Sunrise Hike", "nature")
    ],
    "Yala": [
        ("Yala National Park Safari", "wildlife")
    ],
    "Trincomalee": [
        ("Pigeon Island Snorkeling", "beach"),
        ("Koneswaram Temple Visit", "culture")
    ],
    "Nuwara Eliya": [
        ("Tea Plantation Visit", "tea"),
        ("Gregory Lake Walk", "nature")
    ],
    "Kandy": [
        ("Temple of the Tooth Relic", "culture"),
        ("Cultural Dance Show", "culture")
    ],
    "Colombo": [
        ("Gangaramaya Temple Visit", "culture"),
        ("Colombo City Tour", "city")
    ]
}

# -------------------------------
# WEATHER REGIONS
# -------------------------------
WEATHER_REGION_MAP = {
    "Kalpitiya": "west",
    "Mirissa": "south",
    "Galle": "south",
    "Ella": "hill",
    "Sigiriya": "north",
    "Yala": "south",
    "Trincomalee": "east",
    "Nuwara Eliya": "hill",
    "Kandy": "hill",
    "Colombo": "west"
}

TRAVEL_STYLES = [
    ["solo"],
    ["family"],
    ["friends"],
    ["couple"],
    ["family", "friends"]
]

# -------------------------------
# CLEAN & ENHANCE DATASET
# -------------------------------
with open(INPUT_FILE, "r") as f:
    packages = json.load(f)

cleaned_packages = []

for pkg in packages:
    destinations = pkg.get("destinations", [])
    activities = []

    for dest in destinations:
        if dest in ACTIVITY_MAP:
            name, interest = random.choice(ACTIVITY_MAP[dest])
            activities.append({
                "name": name,
                "interest": interest,
                "duration_hours": random.choice([2, 3]),
                "cost": random.randint(5, 40)
            })

    eco_score = round(random.uniform(0.3, 0.9), 2)

    cleaned_pkg = {
        "id": pkg["id"],
        "destinations": destinations,
        "days": pkg["days"],
        "price": pkg["price"],
        "interests": pkg["interests"],
        "travel_cost": pkg["travel_cost"],
        "hotel_level": pkg["hotel_level"],

        "weather_region": WEATHER_REGION_MAP.get(destinations[0], "mixed"),
        "travel_style": random.choice(TRAVEL_STYLES),
        "eco_score": eco_score,

        "activities": activities
    }

    cleaned_packages.append(cleaned_pkg)

# -------------------------------
# SAVE OUTPUT
# -------------------------------
with open(OUTPUT_FILE, "w") as f:
    json.dump(cleaned_packages, f, indent=2)

print(f"✅ Dataset cleaned successfully!")
print(f"📁 Output file: {OUTPUT_FILE}")
print(f"📊 Total packages: {len(cleaned_packages)}")
