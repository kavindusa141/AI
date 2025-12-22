# agent/explainer.py

def explain(packages, activities, goals):
    """
    Generates human-readable explanation
    for why this plan was selected.
    """

    reasons = []

    # -------------------------------
    # Interest match explanation
    # -------------------------------
    plan_interests = set(i for p in packages for i in p.get("interests", []))
    matched_interests = plan_interests & set(goals["interests"])

    if matched_interests:
        reasons.append(
            f"Matches your interests: {', '.join(matched_interests)}"
        )

    # -------------------------------
    # Budget explanation
    # -------------------------------
    total_cost = sum(p["price"] for p in packages) + sum(a["cost"] for a in activities)

    if total_cost <= goals["budget"]:
        reasons.append(
            f"Fits within your budget (${total_cost} ≤ ${goals['budget']})"
        )
    else:
        reasons.append(
            f"Close to your budget (${total_cost})"
        )

    # -------------------------------
    # Day alignment
    # -------------------------------
    total_days = sum(p["days"] for p in packages)
    reasons.append(
        f"Trip duration is {total_days} days (requested {goals['days']} days)"
    )

    # -------------------------------
    # Activity richness
    # -------------------------------
    if activities:
        reasons.append(
            f"Includes {len(activities)} relevant activities"
        )

    # -------------------------------
    # Diversity
    # -------------------------------
    destinations = set(d for p in packages for d in p.get("destinations", []))
    reasons.append(
        f"Covers {len(destinations)} destinations"
    )

    return reasons
