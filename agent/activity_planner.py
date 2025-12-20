def select_activities(packages, goals):
    selected = []

    max_hours_per_day = 6
    total_days = sum(p["days"] for p in packages)
    max_total_hours = total_days * max_hours_per_day

    # Collect relevant activities
    activities = []
    for p in packages:
        for a in p.get("activities", []):
            if a["interest"] in goals["interests"]:
                activities.append(a)

    # Prefer longer & cheaper activities
    activities.sort(
        key=lambda a: (-a["duration_hours"], a["cost"])
    )

    used_hours = 0

    for a in activities:
        if used_hours + a["duration_hours"] <= max_total_hours:
            selected.append(a)
            used_hours += a["duration_hours"]

    return selected
