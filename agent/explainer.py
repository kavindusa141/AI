import random

def explain(packages, activities, goals):
    """
    Generates a persuasive, human-readable sales pitch 
    for why this plan was selected.
    """
    reasons = []
    
    # 1. Calculate Core Metrics
    total_cost = sum(p["price"] for p in packages) + sum(a.get("cost", 0) for a in activities)
    budget = goals["budget"]
    savings = budget - total_cost
    
    plan_interests = set(i for p in packages for i in p.get("interests", []))
    matched_interests = plan_interests & set(goals["interests"])
    
    destinations = list(set(d for p in packages for d in p.get("destinations", [])))
    
    # -------------------------------
    # 1. THE "HOOK" (Vibe Check)
    # -------------------------------
    # Determine the "Theme" of the trip based on interests
    theme = "A Perfect Getaway"
    if "beach" in matched_interests or "relax" in matched_interests:
        theme = "🌊 A Tropical Relaxation Experience"
    elif "adventure" in matched_interests or "hiking" in matched_interests:
        theme = "🥾 An Adrenaline-Fueled Adventure"
    elif "culture" in matched_interests or "history" in matched_interests:
        theme = "🏛️ A Journey Through History"
    elif "wildlife" in matched_interests:
        theme = "🐘 The Ultimate Wildlife Safari"
        
    reasons.append(f"**{theme}** tailored just for you.")

    # -------------------------------
    # 2. PERSONALIZATION (The "Why You")
    # -------------------------------
    if matched_interests:
        formatted_interests = ", ".join([i.capitalize() for i in matched_interests])
        phrases = [
            f"Curated specifically for your love of {formatted_interests}.",
            f"Heavily focused on {formatted_interests}, just as you requested.",
            f"Designed to hit your top priorities: {formatted_interests}."
        ]
        reasons.append(random.choice(phrases))

    # -------------------------------
    # 3. BUDGET (The "Value Prop")
    # -------------------------------
    if total_cost <= budget:
        if savings > 50:
            reasons.append(f"💰 **Great Value:** You save ${int(savings)}! (Total: ${int(total_cost)})")
        else:
            reasons.append(f"✅ Perfectly fits your budget of ${budget}.")
    else:
        reasons.append(f"💎 Slightly premium, but worth it for the experience (${int(total_cost)}).")

    # -------------------------------
    # 4. PACING & CONTENT (The "Experience")
    # -------------------------------
    avg_acts_per_day = len(activities) / max(goals['days'], 1)
    
    if avg_acts_per_day > 2.5:
        reasons.append("⚡ **Action-Packed:** This itinerary maximizes your time with many experiences.")
    elif avg_acts_per_day < 1.5:
        reasons.append("🍃 **Relaxed Pace:** Plenty of free time to explore at your own rhythm.")
    else:
        reasons.append("⚖️ **Balanced:** A perfect mix of guided activities and leisure time.")

    # -------------------------------
    # 5. DESTINATION HIGHLIGHT (The "Journey")
    # -------------------------------
    if len(destinations) <= 3:
        dest_str = " & ".join(destinations)
        reasons.append(f"📍 Explores the beautiful hubs of {dest_str}.")
    else:
        reasons.append(f"🗺️ A Grand Tour covering {len(destinations)} distinct destinations.")

    # -------------------------------
    # 6. ECO BONUS (The "Feel Good")
    # -------------------------------
    # Check if we have high eco-score packages
    avg_eco = sum(p.get("eco_score", 0.5) for p in packages) / max(len(packages), 1)
    if avg_eco > 0.7:
        reasons.append("🌿 **Eco-Choice:** This trip supports sustainable tourism and green hotels.")

    return reasons