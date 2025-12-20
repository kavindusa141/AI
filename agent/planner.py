from agent.constraints import check_constraints
from itertools import combinations


def generate_candidate_plans(packages, goals):
    candidates = []

    # 🔹 Single-package plans
    for p in packages:
        plan = [p]
        if check_constraints(plan, goals):
            candidates.append(plan)

    # 🔹 Two-package combinations (limited search depth)
    for p1, p2 in combinations(packages, 2):
        plan = [p1, p2]
        if check_constraints(plan, goals):
            candidates.append(plan)

    return candidates
