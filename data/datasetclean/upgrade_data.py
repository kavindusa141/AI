import json

# 1. Define Coordinates for Sri Lankan Cities (Add more if needed)
CITY_COORDS = {
    "Colombo": {"lat": 6.9271, "lon": 79.8612},
    "Kandy": {"lat": 7.2906, "lon": 80.6337},
    "Galle": {"lat": 6.0535, "lon": 80.2210},
    "Sigiriya": {"lat": 7.9570, "lon": 80.7603},
    "Mirissa": {"lat": 5.9482, "lon": 80.4716},
    "Yala": {"lat": 6.3833, "lon": 81.5000},
    "Nuwara Eliya": {"lat": 6.9497, "lon": 80.7891},
    "Ella": {"lat": 6.8667, "lon": 81.0466},
    "Trincomalee": {"lat": 8.5874, "lon": 81.2152},
    "Arugam Bay": {"lat": 6.8427, "lon": 81.8262},
    "Jaffna": {"lat": 9.6615, "lon": 80.0255},
    "Horton Plains": {"lat": 6.8096, "lon": 80.8089},
    "Kalpitiya": {"lat": 8.2295, "lon": 79.7596},
    "Pasikuda": {"lat": 7.9234, "lon": 81.5649},
    "Sinharaja": {"lat": 6.4069, "lon": 80.4578},
    "Anuradhapura": {"lat": 8.3114, "lon": 80.4037},
    "Polonnaruwa": {"lat": 7.9403, "lon": 81.0188}
}

# 2. Heuristic function to guess the best time for an activity
def get_preferred_time(name, interest):
    name = name.lower()
    interest = interest.lower()
    
    if "sunrise" in name or "bird" in name or "yoga" in name:
        return "morning"
    if "sunset" in name or "night" in name or "dinner" in name:
        return "evening"
    if "hike" in name or "trek" in name or "safari" in name or "climb" in name:
        return "morning"  # Better to do physical stuff early
    if "temple" in name:
        return "morning"
    if "museum" in name or "city" in name:
        return "afternoon"
    
    return "any"

# 3. Heuristic to find location coordinates for an activity
def get_activity_coords(activity_name, package_destinations):
    # Try to find city name inside activity name (e.g., "Colombo City Tour")
    for city, coords in CITY_COORDS.items():
        if city.lower() in activity_name.lower():
            return coords
            
    # Fallback: Use the first destination of the package
    for dest in package_destinations:
        if dest in CITY_COORDS:
            return CITY_COORDS[dest]
            
    return {"lat": 6.9271, "lon": 79.8612} # Default to Colombo if unknown

def upgrade_dataset():
    with open('data/tour_packages.json', 'r') as f:
        data = json.load(f)

    for pkg in data:
        destinations = pkg.get('destinations', [])
        
        for activity in pkg.get('activities', []):
            # Add Time Preference
            activity['preferred_time'] = get_preferred_time(activity['name'], activity['interest'])
            
            # Add Coordinates
            coords = get_activity_coords(activity['name'], destinations)
            activity['lat'] = coords['lat']
            activity['lon'] = coords['lon']

    with open('data/tour_packages_new.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    print("✅ Success! Created data/tour_packages_new.json with Lat/Lon and Time.")

if __name__ == "__main__":
    upgrade_dataset()