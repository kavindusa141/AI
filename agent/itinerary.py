def build_itinerary(acts):
    itinerary={}; day=1; hours=8; itinerary[day]=[]
    for a in acts:
        if a['duration_hours']<=hours:
            itinerary[day].append(a); hours-=a['duration_hours']
        else:
            day+=1; hours=8-a['duration_hours']; itinerary[day]=[a]
    return itinerary
