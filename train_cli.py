from agent.agent import TourPlanningAgent

agent = TourPlanningAgent("data/tour_packages.json")

print("=== TOUR PLANNING AI – TRAINING MODE (CMD) ===")

while True:
    try:
        budget = int(input("\nEnter budget (USD): "))
        days = int(input("Enter number of days: "))
        interests = input("Enter interests (comma separated): ").split(",")

        goals = {
            "budget": budget,
            "days": days,
            "interests": [i.strip() for i in interests]
        }

        packages, activities, itinerary = agent.run(goals)

        if packages is None:
            print("\n❌ No feasible plan found.")
            continue

        print("\n🌍 GENERATED TOUR")
        destinations = set()
        total_cost = 0

        for p in packages:
            destinations.update(p["destinations"])
            total_cost += p["price"]

        for a in activities:
            total_cost += a["cost"]

        print("Destinations:", " → ".join(destinations))
        print("Days:", sum(p["days"] for p in packages))
        print("Total Cost:", total_cost)

        print("\n🗓️ Itinerary")
        for day, acts in itinerary.items():
            print(f" Day {day}:")
            for a in acts:
                print(f"  - {a['name']} ({a['interest']})")

        rating = int(input("\nRate this tour (1–5): "))
        agent.learn(packages, activities, goals, rating)

        print("✅ Feedback recorded. Model updated.")

        cont = input("\nTrain again? (y/n): ").lower()
        if cont != "y":
            break

    except Exception as e:
        print("⚠️ Error:", e)

print("\n🎯 Training session ended.")
