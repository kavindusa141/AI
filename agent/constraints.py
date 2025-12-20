def check_constraints(packages, goals):
    total_price = sum(p["price"] for p in packages)
    total_days = sum(p["days"] for p in packages)

    # Budget constraint
    if total_price > goals["budget"]:
        return False

    # 🔥 Enforce exact day match
    if total_days != goals["days"]:
        return False

    # Interest feasibility (at least one match)
    plan_interests = set()
    for p in packages:
        plan_interests.update(p.get("interests", []))

    if not plan_interests.intersection(goals["interests"]):
        return False

    # Avoid duplicate destinations
    destinations = []
    for p in packages:
        destinations.extend(p.get("destinations", []))

    if len(destinations) != len(set(destinations)):
        return False

    return True
