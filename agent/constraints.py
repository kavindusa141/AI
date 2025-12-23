def check_constraints(packages, goals):
    """
    Hard feasibility checks.
    If this fails -> plan is NOT considered at all.
    """

    # 1. Aggregate values
    # Note: This is just the Base Package price. 
    # Activity costs are added later in agent.py, so we leave some buffer here.
    total_price = sum(p.get("price", 0) for p in packages)
    total_days = sum(p.get("days", 0) for p in packages)

    # ======================================================
    # 2. Budget Check (Upper Limit Only)
    # ======================================================
    budget = goals["budget"]
    
    # Allow 10% overflow for the "Base Plan" (AI can trim costs later)
    max_budget = budget * 1.1

    # CRITICAL FIX: Removed the "min_budget" check. 
    # We should never reject a plan because it saves the user money!
    if total_price > max_budget:
        return False

    # ======================================================
    # 3. Day Flexibility (±2 Days)
    # ======================================================
    requested_days = goals["days"]
    
    # We allow a wider gap (±2) during the search phase.
    # If the user asks for 5 days, a 3-day package is fine (we fill it with activities).
    # A 7-day package is also fine (we might cut a day).
    if abs(total_days - requested_days) > 2:
        return False

    # ======================================================
    # 4. Interest Feasibility (Broad Match)
    # ======================================================
    plan_interests = set()
    for p in packages:
        # Collect all interests from the package + its activities
        plan_interests.update(p.get("interests", []))
        for a in p.get("activities", []):
            plan_interests.add(a.get("interest"))

    # If there is ZERO overlap with user goals, reject it.
    user_interests = set(goals["interests"])
    if not plan_interests.intersection(user_interests):
        return False

    # ======================================================
    # 5. Avoid Duplicate Packages
    # ======================================================
    package_ids = [p.get("id") for p in packages]
    if len(package_ids) != len(set(package_ids)):
        return False

    return True