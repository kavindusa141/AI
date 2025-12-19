import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request
from agent.agent import TourPlanningAgent

app = Flask(__name__)
agent = TourPlanningAgent("data/tour_packages.json")


def build_summary(packages, activities):
    destinations = set()
    total_days = 0
    package_cost = 0
    activity_cost = 0

    for p in packages:
        destinations.update(p["destinations"])
        total_days += p["days"]
        package_cost += p["price"]

    for a in activities:
        activity_cost += a["cost"]

    return {
        "destinations": list(destinations),
        "days": total_days,
        "package_cost": package_cost,
        "activity_cost": activity_cost,
        "total_cost": package_cost + activity_cost
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        goals = {
            "budget": int(request.form["budget"]),
            "days": int(request.form["days"]),
            "interests": [i.strip() for i in request.form["interests"].split(",")]
        }

        packages, activities, itinerary = agent.run(goals)

        print("DEBUG → packages:", packages)   # 🔎 DEBUG
        print("DEBUG → activities:", activities)
        print("DEBUG → itinerary:", itinerary)

        if packages is None:
            result = {"error": "No feasible tour plan found."}
        else:
            result = {
                "summary": build_summary(packages, activities),
                "itinerary": itinerary
            }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
