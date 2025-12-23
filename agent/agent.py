from agent.planner import generate_candidate_plans
from agent.activity_planner import select_activities
from agent.itinerary import build_itinerary
from agent.utility import extract_features, rule_based_utility
from agent.explainer import explain
from environment.environment import Environment
from models.nn_model import load_model, train_model
import csv

class TourPlanningAgent:
    def __init__(self, env_path):
        self.env = Environment(env_path)
        self.model = load_model()

    def run(self, goals):
        best_plan = None
        best_activities = None
        best_score = float("-inf")
        best_explanation = {}

        packages = self.env.get_packages()

        # 🔍 SEARCH over candidate plans
        for plan in generate_candidate_plans(packages, goals):

            # --- Select activities ---
            activities = select_activities(plan, goals)

            # --- COST SAFETY CHECK ---
            # Base package cost + Activity costs
            base_cost = sum(p["price"] for p in plan)
            activity_cost = sum(a.get("cost", 0) for a in activities)
            total_cost = base_cost + activity_cost

            if total_cost > goals["budget"]:
                continue

            # --- Feature extraction ---
            features = extract_features(plan, activities, goals)

            # --- Rule-based score ---
            rule_score = rule_based_utility(plan, activities, goals)

            # --- ML score (safe) ---
            ml_score = None
            if self.model:
                try:
                    ml_score = float(self.model.predict([features])[0])
                    # Hybrid Score: 70% Rules, 30% AI
                    score = 0.7 * rule_score + 0.3 * ml_score
                except Exception:
                    score = rule_score
            else:
                score = rule_score

            # --- Select best ---
            if score > best_score:
                best_score = score
                best_plan = plan
                best_activities = activities
                best_explanation = {
                    "rule_score": round(rule_score, 2),
                    "ml_score": round(ml_score, 2) if ml_score is not None else None,
                    "total_cost": total_cost,
                    "reasons": explain(plan, activities, goals)
                }

        # If no valid plan found
        if best_plan is None:
            return None, None, None, None

        # --- Build itinerary ---
        # ⚠️ UPDATED: Now passing a dictionary as expected by the new itinerary.py
        itinerary_data = build_itinerary({
            "activities": best_activities,
            "days": goals["days"],
            "total_cost": best_explanation["total_cost"]
        })

        return best_plan, best_activities, itinerary_data, best_explanation

    def learn(self, plan, activities, goals, rating):
        features = extract_features(plan, activities, goals)

        with open("data/training_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(features + [rating])

        # 🔁 Retrain model
        self.model = train_model()