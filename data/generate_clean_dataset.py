import json
import random

NUM_PACKAGES = 2000
OUTPUT_FILE = "sri_lanka_2000_clean_packages.json"

# ---------------- DESTINATIONS & VALID INTERESTS ----------------
DEST_INTERESTS = {
    "Colombo": ["city", "culture", "shopping"],
    "Galle": ["culture", "beach"],
    "Ella": ["nature", "hiking"],
    "Nuwara Eliya": ["tea", "nature"],
    "Kandy": ["culture", "heritage"],
    "Sigiriya": ["heritage", "culture"],
    "Yala": ["wildlife"],
    "Kalpitiya": ["wildlife", "adventure", "eco"],
    "Arugam Bay": ["surfing", "beach"],
    "Mirissa": ["beach", "wildlife"],
    "Trincomalee": ["beach", "culture"],
    "Pasikuda": ["beach", "luxury"],
    "Jaffna": ["culture", "heritage"],
    "Sinharaja": ["eco", "nature"],
    "Horton Plains": ["hiking", "nature"]
}

# ---------------- REAL ACTIVITIES ----------------
ACTIVITIES = {
    "Kalpitiya": [
        ("Dolphin & Whale Watching", "wildlife", 4, 35),
        ("Kite Surfing Session", "adventure", 3, 40),
        ("Lagoon Kayaking", "eco", 2, 20),
        ("Wilpattu Safari", "wildlife", 6, 75)
    ],
    "Ella": [
        ("Nine Arches Bridge Visit", "nature", 2, 0),
        ("Little Adam’s Peak Hike", "hiking", 3, 0),
        ("Ella Rock Sunrise Hike", "hiking", 5, 10)
    ],
    "Yala": [
        ("Morning Jeep Safari", "wildlife", 4, 55),
        ("Full Day Safari", "wildlife", 8, 80)
    ],
    "Colombo": [
        ("Gangaramaya Temple", "culture", 2, 5),
        ("Colombo City Tour", "city", 4, 20),
        ("Pettah Market Walk", "shopping", 2, 0)
    ],
    "Galle": [
        ("Galle Fort Walking Tour", "culture", 3, 0),
        ("Maritime Museum Visit", "culture", 2, 5)
    ],
    "Nuwara Eliya": [
        ("Tea Factory Tour", "tea", 2, 0),
        ("Gregory Lake Boat Ride", "nature", 2, 15)
    ],
    "Kandy": [
        ("Temple of the Tooth Relic", "culture", 2, 8),
        ("Cultural Dance Show", "culture", 2, 12)
    ],
    "Sigiriya": [
        ("Sigiriya Rock Fortress Climb", "heritage", 4, 36),
        ("Pidurangala Sunrise Hike", "heritage", 3, 5)
    ],
    "Mirissa": [
        ("Whale Watching Boat Tour", "wildlife", 4, 60),
        ("Beach Relaxation", "beach", 3, 0)
    ],
    "Arugam Bay": [
        ("Surfing Lesson", "surfing", 3, 30),
        ("Beach Sunset Walk", "beach", 2, 0)
    ],
    "Trincomalee": [
        ("Pigeon Island Snorkeling", "beach", 4, 45),
        ("Koneswaram Temple Visit", "culture", 2, 0)
    ],
    "Pasikuda": [
        ("Luxury Beach Stay", "luxury", 5, 0),
        ("Snorkeling Experience", "beach", 3, 25)
    ],
    "Jaffna": [
        ("Nallur Kovil Visit", "culture", 2, 0),
        ("Jaffna Fort & Library Tour", "heritage", 3, 0)
    ],
    "Sinharaja": [
        ("Rainforest Guided Trek", "eco", 5, 25)
    ],
    "Horton Plains": [
        ("World’s End Hike", "hiking", 4, 20)
    ]
}

HOTEL_RATES = {
    "budget": 40,
    "eco": 55,
    "mid": 90,
    "luxury": 150
}

def generate_package(pid):
    days = random.randint(2, 7)
    destinations = random.sample(list(DEST_INTERESTS.keys()), random.randint(1, 2))
    hotel_level = random.choice(list(HOTEL_RATES.keys()))
    travel_cost = random.randint(40, 150)

    activities = []
    interests = set()
    activity_cost = 0

    for _ in range(days * 2):
        city = random.choice(destinations)
        act = random.choice(ACTIVITIES[city])
        activities.append({
            "name": act[0],
            "interest": act[1],
            "duration_hours": act[2],
            "cost": act[3]
        })
        interests.add(act[1])
        activity_cost += act[3]

    total_price = (days * HOTEL_RATES[hotel_level]) + travel_cost + activity_cost

    return {
        "id": pid,
        "destinations": destinations,
        "days": days,
        "price": total_price,
        "interests": list(interests),
        "travel_cost": travel_cost,
        "hotel_level": hotel_level,
        "activities": activities
    }

dataset = [generate_package(i) for i in range(1, NUM_PACKAGES + 1)]

with open(OUTPUT_FILE, "w") as f:
    json.dump(dataset, f, indent=2)

print(f"✅ Generated {NUM_PACKAGES} CLEAN tour packages → {OUTPUT_FILE}")
