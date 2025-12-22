def select_activities(packages, goals):
    selected = []

    MAX_HOURS_PER_DAY = 6
    total_days = goals["days"]                 # ✅ FIX
    max_total_hours = total_days * MAX_HOURS_PER_DAY

    # 🔹 Collect matching activities
    activities = []
    for p in packages:
        for a in p.get("activities", []):
            if a["interest"] in goals["interests"]:
                activities.append(a)

    # 🔹 Sort by usefulness
    # Longer duration + reasonable cost
    activities.sort(
        key=lambda a: (-a["duration_hours"], a["cost"])
    )

    used_hours = 0
    interest_counter = {}

    for a in activities:
        interest = a["interest"]

        # ❌ Avoid repeating same interest too much
        if interest_counter.get(interest, 0) >= total_days:
            continue

        if used_hours + a["duration_hours"] <= max_total_hours:
            selected.append(a)
            used_hours += a["duration_hours"]
            interest_counter[interest] = interest_counter.get(interest, 0) + 1

    return selected
