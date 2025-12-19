def check_constraints(pkgs,g):
    return sum(p['price'] for p in pkgs)<=g['budget'] and sum(p['days'] for p in pkgs)<=g['days']
