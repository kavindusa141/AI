from agent.constraints import check_constraints
from itertools import permutations, product

def generate_candidate_plans(packages, goals):
    """
    Generates feasible tour plans using limited-depth search.
    Now considers ORDER of packages (e.g., City -> Beach vs Beach -> City).
    """

    candidates = []
    target_days = goals["days"]

    # ======================================================
    # 1. Single-package plans (Simple)
    # ======================================================
    for p in packages:
        plan = [p]
        if check_constraints(plan, goals):
            candidates.append(plan)

    # ======================================================
    # 2. Two-package Permutations (Complexity: High)
    # ======================================================
    # We use 'permutations' instead of 'combinations' because 
    # [Kandy, Galle] is a different trip than [Galle, Kandy].
    for p1, p2 in permutations(packages, 2):
        
        # Fast Pruning: Don't check constraints if days are way off
        # Matches the ±2 logic in constraints.py
        total_days = p1["days"] + p2["days"]
        if total_days > target_days + 2:
            continue
        if total_days < target_days - 2:
            continue

        plan = [p1, p2]
        if check_constraints(plan, goals):
            candidates.append(plan)

    # ======================================================
    # 3. Three-package Permutations (Adaptive Depth)
    # ======================================================
    # Only try this if the user wants a LONG trip (> 8 days)
    # otherwise it's too slow for a demo.
    if target_days > 8:
        # We limit the search to top 30 packages to prevent crashing
        top_packages = sorted(packages, key=lambda x: x['price'])[:30]
        
        for p1, p2, p3 in permutations(top_packages, 3):
            if (p1["days"] + p2["days"] + p3["days"]) > target_days + 2:
                continue
            
            plan = [p1, p2, p3]
            if check_constraints(plan, goals):
                candidates.append(plan)

    return candidates