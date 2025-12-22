# agent/eco_score.py

def eco_score(packages):
    """
    Eco friendliness scoring (0–1)
    """
    score = 0

    for p in packages:
        hotel = p.get("hotel_level", "mid")

        if hotel in ("eco", "budget"):
            score += 1
        elif hotel == "mid":
            score += 0.5

    return score / max(len(packages), 1)
