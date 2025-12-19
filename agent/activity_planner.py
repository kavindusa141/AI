def select_activities(pkgs,g):
    return [a for p in pkgs for a in p.get('activities',[]) if a['interest'] in g['interests']]
