def build_itinerary(activities, requested_days):
    itinerary = {}
    daily_costs = {}

    MAX_HOURS_PER_DAY = 6
    day = 1
    remaining_hours = MAX_HOURS_PER_DAY

    itinerary[day] = []
    daily_costs[day] = 0

    for a in activities:
        duration = a["duration_hours"]

        # Skip impossible activities
        if duration > MAX_HOURS_PER_DAY:
            continue

        # If activity fits in current day
        if duration <= remaining_hours:
            itinerary[day].append(a)
            daily_costs[day] += a["cost"]
            remaining_hours -= duration
        else:
            # Move to next day
            day += 1
            if day > requested_days:
                break

            remaining_hours = MAX_HOURS_PER_DAY
            itinerary[day] = [a]
            daily_costs[day] = a["cost"]
            remaining_hours -= duration

    # 🔹 Fill missing days with rest
    while day < requested_days:
        day += 1
        itinerary[day] = [{
            "name": "Free Day / Relax",
            "interest": "flex",
            "duration_hours": 3,
            "cost": 0
        }]
        daily_costs[day] = 0

    return itinerary, daily_costs
