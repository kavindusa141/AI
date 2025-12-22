from agent.agent import TourPlanningAgent

# Initialize agent with environment
agent = TourPlanningAgent("data/tour_packages.json")

print("=== TOUR PLANNING AI – TRAINING MODE (CMD) ===")

while True:
    try:
        # 🔹 User input
        budget = int(input("\nEnter budget (USD): "))
        days = int(input("Enter number of days: "))
        interests = input("Enter interests (comma separated): ").split(",")

        goals = {
            "budget": budget,
            "days": days,
            "interests": [i.strip() for i in interests if i.strip()],
            "traveler_type": "default"  # safe default
        }

        # 🔹 Run agent (UPDATED)
        packages, activities, itinerary, explanation = agent.run(goals)

        if packages is None:
            print("\n❌ No feasible plan found.")
            continue

        # ----------------------------
        # 🌍 SUMMARY
        # ----------------------------
        print("\n🌍 GENERATED TOUR")

        destinations = set()
        total_cost = 0

        for p in packages:
            destinations.update(p["destinations"])
            total_cost += p["price"]

        for a in activities:
            total_cost += a["cost"]

        print("Destinations:", " → ".join(destinations))
        print("Days:", goals["days"])
        print("Total Cost (USD):", total_cost)

        # ----------------------------
        # 🗓️ ITINERARY
        # ----------------------------
        print("\n🗓️ Itinerary")

        for day in sorted(itinerary):
            day_cost = 0
            print(f" Day {day}:")
            for a in itinerary[day]:
                print(f"  - {a['name']} ({a['interest']}, {a['duration_hours']}h)")
                day_cost += a.get("cost", 0)
            print(f"   Day Cost: ${day_cost}")

        # ----------------------------
        # 🧠 EXPLANATION
        # ----------------------------
        print("\n🧠 Why this tour was recommended:")
        for r in explanation["reasons"]:
            print(" •", r)

        print("\nScores:")
        print(" Rule Score:", explanation["rule_score"])
        print(" ML Score:", explanation["ml_score"])
        print(" Estimated Total Cost:", explanation["total_cost"])

        # ----------------------------
        # ⭐ FEEDBACK
        # ----------------------------
        while True:
            rating = int(input("\nRate this tour (1–5): "))
            if 1 <= rating <= 5:
                break
            print("⚠️ Please enter a rating between 1 and 5.")

        agent.learn(packages, activities, goals, rating)

        print("✅ Feedback recorded.")
        print("🧠 Model updated using user feedback.")

        cont = input("\nTrain again? (y/n): ").lower()
        if cont != "y":
            break

    except Exception as e:
        print("⚠️ Error:", e)

print("\n🎯 Training session ended.")
