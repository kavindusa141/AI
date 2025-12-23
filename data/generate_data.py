import json
import random

# ==========================================
# 1. MASTER DATA: CITIES & COORDINATES
# ==========================================
CITIES = {
    "Colombo": {"lat": 6.9271, "lon": 79.8612},
    "Kandy": {"lat": 7.2906, "lon": 80.6337},
    "Galle": {"lat": 6.0535, "lon": 80.2210},
    "Sigiriya": {"lat": 7.9570, "lon": 80.7603},
    "Mirissa": {"lat": 5.9482, "lon": 80.4716},
    "Yala": {"lat": 6.3833, "lon": 81.5000},
    "Nuwara Eliya": {"lat": 6.9497, "lon": 80.7891},
    "Ella": {"lat": 6.8667, "lon": 81.0466},
    "Trincomalee": {"lat": 8.5874, "lon": 81.2152},
    "Anuradhapura": {"lat": 8.3114, "lon": 80.4037},
    "Bentota": {"lat": 6.4290, "lon": 79.9973}
}

# ==========================================
# 2. MASTER DATA: ACTIVITIES POOL
# ==========================================
# Each city has a list of possible activities with specific details.
ACTIVITIES_DB = {
    "Colombo": [
        {"name": "Gangaramaya Temple", "interest": "culture", "duration": 2, "cost": 5, "time": "morning"},
        {"name": "Lotus Tower Deck", "interest": "city", "duration": 2, "cost": 20, "time": "evening"},
        {"name": "Pettah Market Walk", "interest": "city", "duration": 2, "cost": 0, "time": "morning"},
        {"name": "National Museum", "interest": "culture", "duration": 3, "cost": 10, "time": "afternoon"},
        {"name": "Galle Face Green Sunset", "interest": "relax", "duration": 2, "cost": 0, "time": "evening"},
        {"name": "Independence Square", "interest": "history", "duration": 1, "cost": 0, "time": "any"}
    ],
    "Kandy": [
        {"name": "Temple of Tooth Relic", "interest": "culture", "duration": 2, "cost": 15, "time": "morning"},
        {"name": "Peradeniya Botanical Garden", "interest": "nature", "duration": 3, "cost": 10, "time": "morning"},
        {"name": "Kandy Lake Walk", "interest": "relax", "duration": 1, "cost": 0, "time": "evening"},
        {"name": "Cultural Dance Show", "interest": "culture", "duration": 2, "cost": 12, "time": "evening"},
        {"name": "Bahirawakanda Buddha", "interest": "culture", "duration": 1, "cost": 3, "time": "afternoon"}
    ],
    "Nuwara Eliya": [
        {"name": "Gregory Lake Boat Ride", "interest": "relax", "duration": 2, "cost": 10, "time": "afternoon"},
        {"name": "Tea Factory Visit", "interest": "culture", "duration": 2, "cost": 5, "time": "morning"},
        {"name": "Horton Plains Hike", "interest": "nature", "duration": 4, "cost": 35, "time": "morning"},
        {"name": "Victoria Park", "interest": "nature", "duration": 1, "cost": 2, "time": "any"},
        {"name": "Strawberry Farm Visit", "interest": "food", "duration": 1, "cost": 5, "time": "afternoon"}
    ],
    "Ella": [
        {"name": "Nine Arch Bridge", "interest": "photography", "duration": 2, "cost": 0, "time": "morning"},
        {"name": "Little Adam's Peak", "interest": "hiking", "duration": 3, "cost": 0, "time": "morning"},
        {"name": "Ella Rock Hike", "interest": "hiking", "duration": 4, "cost": 0, "time": "morning"},
        {"name": "Ravana Falls", "interest": "nature", "duration": 1, "cost": 0, "time": "afternoon"},
        {"name": "Cookery Class", "interest": "food", "duration": 3, "cost": 25, "time": "evening"}
    ],
    "Sigiriya": [
        {"name": "Sigiriya Rock Fortress", "interest": "history", "duration": 4, "cost": 30, "time": "morning"},
        {"name": "Pidurangala Rock Sunrise", "interest": "adventure", "duration": 3, "cost": 5, "time": "morning"},
        {"name": "Village Safari Tour", "interest": "culture", "duration": 2, "cost": 15, "time": "afternoon"},
        {"name": "Minneriya Elephant Safari", "interest": "wildlife", "duration": 4, "cost": 50, "time": "afternoon"}
    ],
    "Galle": [
        {"name": "Galle Fort Walk", "interest": "history", "duration": 3, "cost": 0, "time": "afternoon"},
        {"name": "Maritime Museum", "interest": "culture", "duration": 2, "cost": 5, "time": "morning"},
        {"name": "Lighthouse Visit", "interest": "photography", "duration": 1, "cost": 0, "time": "evening"},
        {"name": "Unawatuna Beach", "interest": "beach", "duration": 4, "cost": 0, "time": "any"}
    ],
    "Mirissa": [
        {"name": "Whale Watching", "interest": "wildlife", "duration": 5, "cost": 70, "time": "morning"},
        {"name": "Coconut Tree Hill", "interest": "photography", "duration": 1, "cost": 0, "time": "evening"},
        {"name": "Secret Beach", "interest": "beach", "duration": 3, "cost": 0, "time": "afternoon"},
        {"name": "Surfing Lesson", "interest": "adventure", "duration": 2, "cost": 20, "time": "morning"}
    ],
    "Yala": [
        {"name": "Yala National Park Safari", "interest": "wildlife", "duration": 5, "cost": 60, "time": "morning"},
        {"name": "Sithulpawwa Temple", "interest": "culture", "duration": 2, "cost": 0, "time": "afternoon"},
        {"name": "Camping Experience", "interest": "adventure", "duration": 12, "cost": 150, "time": "evening"}
    ],
    "Trincomalee": [
        {"name": "Nilaveli Beach", "interest": "beach", "duration": 4, "cost": 0, "time": "morning"},
        {"name": "Koneswaram Temple", "interest": "culture", "duration": 2, "cost": 0, "time": "morning"},
        {"name": "Pigeon Island Snorkeling", "interest": "adventure", "duration": 4, "cost": 40, "time": "morning"}
    ],
    "Anuradhapura": [
        {"name": "Ruwanwelisaya Stupa", "interest": "history", "duration": 2, "cost": 0, "time": "morning"},
        {"name": "Sri Maha Bodhi", "interest": "culture", "duration": 1, "cost": 0, "time": "morning"},
        {"name": "Isurumuniya Temple", "interest": "history", "duration": 1, "cost": 2, "time": "afternoon"}
    ],
    "Bentota": [
        {"name": "Water Sports", "interest": "adventure", "duration": 3, "cost": 40, "time": "morning"},
        {"name": "River Safari", "interest": "nature", "duration": 2, "cost": 15, "time": "afternoon"},
        {"name": "Turtle Hatchery", "interest": "wildlife", "duration": 1, "cost": 5, "time": "any"}
    ]
}

# ==========================================
# 3. ROUTE TEMPLATES (LOGICAL TRIPS)
# ==========================================
ROUTES = [
    {"name": "Hill Country", "cities": ["Kandy", "Nuwara Eliya", "Ella"]},
    {"name": "Southern Coast", "cities": ["Galle", "Mirissa", "Yala"]},
    {"name": "Cultural Triangle", "cities": ["Anuradhapura", "Sigiriya", "Kandy"]},
    {"name": "City & Beach", "cities": ["Colombo", "Bentota", "Galle"]},
    {"name": "East Coast Explorer", "cities": ["Sigiriya", "Trincomalee"]},
    {"name": "Ultimate Lanka", "cities": ["Colombo", "Sigiriya", "Kandy", "Ella", "Yala", "Mirissa"]}
]

# ==========================================
# 4. GENERATOR LOGIC
# ==========================================
def generate_packages(count=100):
    packages = []
    package_id = 1

    for _ in range(count):
        # 1. Pick a random route
        route = random.choice(ROUTES)
        selected_cities = route["cities"]
        
        # 2. Randomize Days (Approx 1-2 days per city)
        min_days = len(selected_cities)
        max_days = len(selected_cities) * 2
        days = random.randint(min_days, max_days)
        
        # 3. Collect Activities
        package_activities = []
        package_interests = set()
        total_activity_cost = 0

        for city in selected_cities:
            # Get activities for this city
            if city in ACTIVITIES_DB:
                city_acts = ACTIVITIES_DB[city]
                # Randomly pick 2-4 activities per city
                picked = random.sample(city_acts, k=min(len(city_acts), random.randint(2, 4)))
                
                for act in picked:
                    # Enrich with Geo Data
                    enriched_act = act.copy()
                    enriched_act["lat"] = CITIES[city]["lat"]
                    enriched_act["lon"] = CITIES[city]["lon"]
                    
                    # Rename activity to include city for clarity (optional)
                    # enriched_act["name"] = f"{act['name']} ({city})"
                    
                    package_activities.append(enriched_act)
                    package_interests.add(act["interest"])
                    total_activity_cost += act["cost"]

        # 4. Calculate Price
        # Base cost per day (hotel + travel)
        hotel_level = random.choice(["budget", "standard", "luxury"])
        base_cost_per_day = {"budget": 50, "standard": 100, "luxury": 200}[hotel_level]
        
        total_price = (base_cost_per_day * days) + total_activity_cost

        # 5. Create Package Object
        pkg = {
            "id": package_id,
            "destinations": selected_cities,
            "days": days,
            "price": int(total_price),
            "interests": list(package_interests),
            "hotel_level": hotel_level,
            "travel_style": random.choice(["solo", "family", "adventure", "relax"]),
            "eco_score": round(random.uniform(0.3, 0.9), 2),
            "activities": package_activities
        }
        
        packages.append(pkg)
        package_id += 1

    return packages

# ==========================================
# 5. EXECUTION
# ==========================================
if __name__ == "__main__":
    print("🚀 Generating Tour Packages...")
    data = generate_packages(1000) # Generate 1000 unique packages
    
    file_path = "tour_packages.json"
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"✅ Successfully generated {len(data)} packages in '{file_path}'")
    print("Includes: Lat/Lon, Time Preferences, and Logic-based Routing.")