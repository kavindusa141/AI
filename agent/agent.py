from agent.planner import generate_candidate_plans
from agent.activity_planner import select_activities
from agent.itinerary import build_itinerary
from agent.utility import extract_features, rule_based_utility
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

        packages = self.env.get_packages()

        # 🔍 SEARCH over candidate plans
        for plan in generate_candidate_plans(packages, goals):

            activities = select_activities(plan, goals)
            features = extract_features(plan, activities, goals)

            # 🧠 HYBRID DECISION
            if self.model:
                score = self.model.predict([features])[0]
            else:
                score = rule_based_utility(plan, activities, goals)

            if score > best_score:
                best_score = score
                best_plan = plan
                best_activities = activities

        if best_plan is None:
            return None, None, None, None

        # ✅ FIX: enforce full-day itinerary
        itinerary, daily_costs = build_itinerary(
            best_activities,
            goals["days"]
        )

        return best_plan, best_activities, itinerary, daily_costs

    def learn(self, plan, activities, goals, rating):
        features = extract_features(plan, activities, goals)

        with open("data/training_data.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(features + [rating])

        # 🔁 Retrain model after feedback
        self.model = train_model()
