def rule_based_utility(pkgs,acts,g):
    interests=set(i for p in pkgs for i in p['interests'])
    interest_score=len(set(g['interests']) & interests)/len(g['interests'])
    cost=sum(p['price'] for p in pkgs)
    budget_score=1-cost/g['budget']
    return interest_score*0.6 + budget_score*0.4

def extract_features(pkgs,acts,g):
    cost=sum(p['price'] for p in pkgs)
    days=sum(p['days'] for p in pkgs)
    travel=sum(p['travel_cost'] for p in pkgs)
    interests=set(i for p in pkgs for i in p['interests'])
    im=len(set(g['interests']) & interests)/len(g['interests'])
    am=len([a for a in acts if a['interest'] in g['interests']])/max(len(acts),1)
    return [cost,days,travel,im,am]
