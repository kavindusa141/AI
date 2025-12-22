def check_constraints(packages, goals):
    """
    Hard feasibility checks.
    If this fails → plan is NOT considered at all.
    """

    # 🔹 Aggregate values
    total_price = sum(p.get("price", 0) for p in packages)
    total_days = sum(p.get("days", 0) for p in packages)

    # ======================================================
    # 1️⃣ Budget Elasticity (±10%)
    # ======================================================
    budget = goals["budget"]
    min_budget = budget * 0.9
    max_budget = budget * 1.1

    if total_price < min_budget or total_price > max_budget:
        return False

    # ======================================================
    # 2️⃣ Day Flexibility (±1 day)
    # ======================================================
    requested_days = goals["days"]
    if abs(total_days - requested_days) > 1:
        return False

    # ======================================================
    # 3️⃣ Interest Feasibility (at least one overlap)
    # ======================================================
    plan_interests = set()
    for p in packages:
        plan_interests.update(p.get("interests", []))

    if not plan_interests.intersection(set(goals["interests"])):
        return False

    # ======================================================
    # 4️⃣ Avoid duplicate packages
    # ======================================================
    package_ids = [p.get("id") for p in packages]
    if len(package_ids) != len(set(package_ids)):
        return False

    return True
