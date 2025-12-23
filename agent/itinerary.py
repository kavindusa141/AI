def build_itinerary(plan_data):
    # 1. Unpack Input
    # We expect plan_data to contain 'activities' (list) and 'days' (int)
    activities = plan_data.get('activities', [])
    requested_days = plan_data.get('days', 3)
    
    itinerary = []     # Output: List of Lists (Day 1, Day 2...)
    daily_costs = {}
    
    # 2. Setup
    MAX_HOURS_PER_DAY = 10 # Allow full days
    current_day_acts = []
    current_day_hours = 0
    
    # Time Order for sorting: Morning (0) -> Afternoon (1) -> Evening (2) -> Any (3)
    time_order = {"morning": 0, "afternoon": 1, "evening": 2, "any": 3}

    # 3. Fill Days
    for a in activities:
        duration = a.get("duration_hours", 2) # Safety default
        
        # Check if adding this activity exceeds the day limit
        if current_day_hours + duration > MAX_HOURS_PER_DAY:
            # Day is full! 
            # A. Sort the current day by Preferred Time (Morning -> Evening)
            current_day_acts.sort(key=lambda x: time_order.get(x.get('preferred_time', 'any'), 3))
            
            # B. Save Day and Reset
            itinerary.append(current_day_acts)
            current_day_acts = []
            current_day_hours = 0
            
            # Stop if we have filled all requested days
            if len(itinerary) >= requested_days:
                break

        # Add activity to current buffer
        current_day_acts.append(a)
        current_day_hours += duration

    # 4. Handle the last partial day
    if current_day_acts and len(itinerary) < requested_days:
        current_day_acts.sort(key=lambda x: time_order.get(x.get('preferred_time', 'any'), 3))
        itinerary.append(current_day_acts)

    # 5. Fill Empty Days (if any)
    # If user asked for 5 days but we only had activities for 3, add "Free Days"
    while len(itinerary) < requested_days:
        itinerary.append([{
            "name": "Free Day / Relax", 
            "interest": "flex", 
            "duration_hours": 0, 
            "cost": 0, 
            "preferred_time": "any",
            # Add dummy lat/lon so Map doesn't crash
            "lat": 6.9271, 
            "lon": 79.8612 
        }])

    # 6. Final Calculation
    total_cost = sum(a.get('cost', 0) for day in itinerary for a in day)

    return {
        "daily_activities": itinerary,
        "total_cost": total_cost,
        "daily_costs": {i+1: sum(a.get('cost',0) for a in day) for i, day in enumerate(itinerary)}
    }