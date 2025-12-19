from agent.planner import generate_candidate_plans
from agent.activity_planner import select_activities
from agent.itinerary import build_itinerary
from agent.utility import extract_features, rule_based_utility
from environment.environment import Environment
from models.nn_model import load_model, train_model
import csv

class TourPlanningAgent:
    def __init__(self,env):
        self.env=Environment(env)
        self.model=load_model()

    def run(self,g):
        best=None; best_score=-1
        for plan in generate_candidate_plans(self.env.get_packages(), g):
            acts=select_activities(plan,g)
            score=self.model.predict([extract_features(plan,acts,g)])[0] if self.model else rule_based_utility(plan,acts,g)
            if score>best_score:
                best_score=score; best=(plan,acts)
        if best is None:
            return None,None,None
        return best[0], best[1], build_itinerary(best[1])

    def learn(self,plan,acts,g,rating):
        with open('data/training_data.csv','a',newline='') as f:
            csv.writer(f).writerow(extract_features(plan,acts,g)+[rating])
        self.model=train_model()
