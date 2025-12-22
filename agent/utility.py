# agent/utility.py

from environment.weather import get_weather
from agent.eco_score import eco_score
from agent.traveler_profile import get_profile_weights


def rule_based_utility(packages, activities, goals):
    """
    Hybrid rule-based utility function.
    Exam-safe, explainable, and extensible.
    """

    # ===============================
    # Interest match
    # ===============================
    plan_interests = set(i for p in packages for i in p.get("interests", []))
    interest_score = len(plan_interests & set(goals["interests"])) / max(len(goals["interests"]), 1)

    # ===============================
    # Activity relevance
    # ===============================
    relevant_acts = [a for a in activities if a["interest"] in goals["interests"]]
    activity_score = len(relevant_acts) / max(len(activities), 1)

    # ===============================
    # Budget elasticity
    # ===============================
    total_cost = sum(p["price"] for p in packages) + sum(a["cost"] for a in activities)
    budget_ratio = total_cost / goals["budget"]
    budget_efficiency = max(0, 1 - abs(1 - budget_ratio))

    # ===============================
    # Day flexibility
    # ===============================
    total_days = sum(p["days"] for p in packages)
    day_ratio = total_days / goals["days"]
    day_efficiency = max(0, 1 - abs(1 - day_ratio))

    # ===============================
    # Weather awareness
    # ===============================
    weather_hits = 0
    for p in packages:
        weather = get_weather(p.get("region", "mixed"))
        if weather in ("dry", "cool"):
            weather_hits += 1
    weather_score = weather_hits / max(len(packages), 1)

    # ===============================
    # Eco friendliness
    # ===============================
    eco = eco_score(packages)

    # ===============================
    # Traveler profile
    # ===============================
    profile = goals.get("traveler_type", "default")
    weights = get_profile_weights(profile)

    # ===============================
    # Final weighted score
    # ===============================
    return (
        interest_score * 0.35 +
        activity_score * weights["activity_weight"] +
        budget_efficiency * 0.2 +
        day_efficiency * 0.1 +
        weather_score * 0.1 +
        eco * weights["eco_weight"]
    )


def extract_features(packages, activities, goals):
    """
    ML feature vector (normalized, stable)
    """

    total_cost = sum(p["price"] for p in packages)
    total_days = sum(p["days"] for p in packages)
    total_travel = sum(p["travel_cost"] for p in packages)

    plan_interests = set(i for p in packages for i in p.get("interests", []))

    interest_match = len(plan_interests & set(goals["interests"])) / max(len(goals["interests"]), 1)
    activity_match = len([a for a in activities if a["interest"] in goals["interests"]]) / max(len(activities), 1)

    return [
        total_cost / goals["budget"],
        total_days / goals["days"],
        total_travel / max(goals["budget"], 1),
        interest_match,
        activity_match
    ]
