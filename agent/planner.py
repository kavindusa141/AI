from agent.constraints import check_constraints
from itertools import combinations


def generate_candidate_plans(packages, goals):
    """
    Generates feasible tour plans using limited-depth search.
    Uses constraint filtering to avoid invalid plans early.
    """

    candidates = []

    # ======================================================
    # 1️⃣ Single-package plans
    # ======================================================
    for p in packages:
        plan = [p]
        if check_constraints(plan, goals):
            candidates.append(plan)

    # ======================================================
    # 2️⃣ Two-package combinations (safe & exam-friendly)
    # ======================================================
    for p1, p2 in combinations(packages, 2):
        plan = [p1, p2]

        # Quick pruning: skip if days already too large
        if p1["days"] + p2["days"] > goals["days"] + 1:
            continue

        if check_constraints(plan, goals):
            candidates.append(plan)

    return candidates
