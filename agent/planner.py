from agent.constraints import check_constraints
def generate_candidate_plans(pkgs,g):
    return [[p] for p in pkgs if check_constraints([p],g)]
