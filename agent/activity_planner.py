def select_activities(pkgs, g):
    selected = []
    
    # 1. Setup Constraints
    MAX_HOURS_PER_DAY = 10  # Increased to allow full days
    total_days = g["days"]
    max_total_hours = total_days * MAX_HOURS_PER_DAY

    # 2. Get ALL activities from all packages
    all_activities = [a for p in pkgs for a in p.get('activities', [])]

    # ---------------------------------------------------------
    # DATA FIX: Normalize 'duration' vs 'duration_hours'
    # The new dataset uses "duration", old code uses "duration_hours".
    # We standardize everything to "duration_hours" here.
    # ---------------------------------------------------------
    for a in all_activities:
        if 'duration' in a and 'duration_hours' not in a:
            a['duration_hours'] = a['duration']
    # ---------------------------------------------------------

    # 3. Categorize by Interest Match
    # Priority A: Matches User Interest
    # Priority B: General/Popular (Backup)
    priority_acts = [a for a in all_activities if a["interest"] in g["interests"]]
    backup_acts = [a for a in all_activities if a["interest"] not in g["interests"]]

    # 4. Sort Logic
    # Sort by Duration (Longer first) and Cost (Higher cost = Higher Value/Quality)
    priority_acts.sort(key=lambda a: (-a.get("duration_hours", 0), -a.get("cost", 0)))
    
    # Sort backups by general quality (cost)
    backup_acts.sort(key=lambda a: -a.get("cost", 0))

    # 5. Selection Logic
    used_hours = 0
    interest_counter = {}

    def try_add(activity_list):
        nonlocal used_hours
        for a in activity_list:
            interest = a["interest"]
            duration = a.get("duration_hours", 2) # Default to 2h if missing
            
            # Diversity Check: Don't overdose on one interest (limit 3 per type)
            if interest_counter.get(interest, 0) >= 3: 
                continue

            if used_hours + duration <= max_total_hours:
                selected.append(a)
                used_hours += duration
                interest_counter[interest] = interest_counter.get(interest, 0) + 1

    # First: Fill with User's Interests
    try_add(priority_acts)
    
    # Second: If schedule is empty or light (less than 70% full), fill with high-quality backups
    if used_hours < (max_total_hours * 0.7):
        try_add(backup_acts)

    return selected
