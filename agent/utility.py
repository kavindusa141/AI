def rule_based_utility(packages, activities, goals):
    # 🔹 Interest match score
    plan_interests = set(i for p in packages for i in p["interests"])
    interest_score = len(plan_interests & set(goals["interests"])) / max(len(goals["interests"]), 1)

    # 🔹 Activity relevance score
    activity_match = len([a for a in activities if a["interest"] in goals["interests"]])
    activity_score = activity_match / max(len(activities), 1)

    # 🔹 Budget closeness score (near budget is better)
    total_cost = sum(p["price"] for p in packages)
    budget_ratio = total_cost / goals["budget"]
    budget_efficiency = max(0, 1 - abs(1 - budget_ratio))

    # 🔹 Day match score (exact match enforced by constraints)
    total_days = sum(p["days"] for p in packages)
    day_efficiency = 1 if total_days == goals["days"] else 0

    # 🔹 Final weighted utility
    return (
        interest_score * 0.4 +
        activity_score * 0.3 +
        budget_efficiency * 0.2 +
        day_efficiency * 0.1
    )


def extract_features(packages, activities, goals):
    total_cost = sum(p["price"] for p in packages)
    total_days = sum(p["days"] for p in packages)
    total_travel = sum(p["travel_cost"] for p in packages)

    plan_interests = set(i for p in packages for i in p["interests"])

    interest_match = len(plan_interests & set(goals["interests"])) / max(len(goals["interests"]), 1)
    activity_match = len([a for a in activities if a["interest"] in goals["interests"]]) / max(len(activities), 1)

    # 🔹 Normalized numeric features (for ML)
    norm_cost = total_cost / goals["budget"]
    norm_days = total_days / goals["days"]
    norm_travel = total_travel / max(goals["budget"], 1)

    return [
        norm_cost,
        norm_days,
        norm_travel,
        interest_match,
        activity_match
    ]
