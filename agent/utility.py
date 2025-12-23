from environment.weather import get_weather
# Ensure this matches the function name in agent/eco_score.py
from agent.eco_score import calculate_eco_score 
from agent.traveler_profile import get_profile_weights

def rule_based_utility(packages, activities, goals):
    """
    Hybrid rule-based utility function.
    Exam-safe, explainable, and extensible.
    """
    # 1. Interest match
    plan_interests = set(i for p in packages for i in p.get("interests", []))
    interest_score = len(plan_interests & set(goals["interests"])) / max(len(goals["interests"]), 1)

    # 2. Activity relevance
    relevant_acts = [a for a in activities if a["interest"] in goals["interests"]]
    activity_score = len(relevant_acts) / max(len(activities), 1)

    # 3. Budget Score (Higher is better)
    # We prioritize being UNDER budget. 
    total_cost = sum(p["price"] for p in packages) + sum(a.get("cost", 0) for a in activities)
    
    if total_cost <= goals["budget"]:
        # Score 1.0 if perfectly under budget
        budget_score = 1.0
    else:
        # Score drops as you go over budget
        overage = total_cost - goals["budget"]
        budget_score = max(0, 1 - (overage / goals["budget"]))

    # 4. Day flexibility
    total_days = sum(p["days"] for p in packages)
    day_ratio = total_days / goals["days"]
    day_efficiency = max(0, 1 - abs(1 - day_ratio))

    # 5. Weather awareness
    weather_hits = 0
    for p in packages:
        # Default to 'mixed' if region is missing
        region = p.get("weather_region", "mixed") 
        weather = get_weather(region)
        if weather in ("sunny", "cool"):
            weather_hits += 1
    weather_score = weather_hits / max(len(packages), 1)

    # 6. Eco friendliness
    eco = calculate_eco_score(packages)

    # 7. Traveler profile (Dynamic Weights)
    # ⚠️ FIXED: Matches 'travel_style' from ui/app.py
    profile = goals.get("travel_style", "default") 
    weights = get_profile_weights(profile)

    # --- Final weighted score ---
    return (
        interest_score * 0.30 +
        activity_score * weights["activity_weight"] +
        budget_score * 0.20 +
        day_efficiency * 0.10 +
        weather_score * 0.10 +
        eco * weights["eco_weight"]
    )

def extract_features(packages, activities, goals):
    """
    ML feature vector (normalized, stable)
    """
    total_cost = sum(p["price"] for p in packages) + sum(a.get("cost", 0) for a in activities)
    total_days = sum(p["days"] for p in packages)
    # Some packages might not have travel_cost, default to 0
    total_travel = sum(p.get("travel_cost", 0) for p in packages)

    plan_interests = set(i for p in packages for i in p.get("interests", []))

    interest_match = len(plan_interests & set(goals["interests"])) / max(len(goals["interests"]), 1)
    activity_match = len([a for a in activities if a["interest"] in goals["interests"]]) / max(len(activities), 1)

    # Returns 5 features
    return [
        total_cost / max(goals["budget"], 1),
        total_days / max(goals["days"], 1),
        total_travel / max(goals["budget"], 1),
        interest_match,
        activity_match
    ]