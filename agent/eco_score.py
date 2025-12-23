def calculate_eco_score(packages):
    """
    Calculates the average Eco Score of a plan (0.0 to 1.0).
    It looks for the explicit 'eco_score' in the data first.
    If missing, it estimates based on 'hotel_level'.
    """
    total_score = 0
    
    for p in packages:
        # Priority 1: Use the real data field (from generate_data.py)
        if "eco_score" in p:
            total_score += p["eco_score"]
        
        # Priority 2: Guess based on hotel type (Fallback)
        else:
            hotel = p.get("hotel_level", "standard")
            
            if hotel == "budget": 
                total_score += 0.8  # Budget usually means less energy consumption
            elif hotel == "standard": 
                total_score += 0.5
            elif hotel == "luxury":
                total_score += 0.3  # Luxury often has high carbon footprint
            else:
                total_score += 0.5

    # Return Average
    return total_score / max(len(packages), 1)