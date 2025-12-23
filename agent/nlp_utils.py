# agent/nlp_utils.py
import re

def extract_interests_from_text(text):
    """
    Scans user text for keywords and maps them to known categories.
    """
    text = text.lower()
    
    # 1. Define your "Knowledge Base" (Synonyms -> Category)
    # The 'Category' must match tags in tour_packages.json
    keyword_map = {
        "culture": ["history", "temple", "ruins", "ancient", "museum", "art", "heritage", "buddhist"],
        "nature": ["forest", "mountain", "hike", "trek", "waterfall", "bird", "green", "tea"],
        "wildlife": ["safari", "elephant", "leopard", "animals", "zoo", "park"],
        "beach": ["sea", "ocean", "swim", "sand", "surf", "coastal", "sun"],
        "relax": ["chill", "spa", "massage", "quiet", "leisure", "resort"],
        "city": ["shopping", "urban", "food", "street", "nightlife", "colombo"],
        "adventure": ["rafting", "diving", "climb", "adrenaline", "sport"]
    }
    
    detected = set()
    
    # 2. Check for direct matches or synonyms
    for category, keywords in keyword_map.items():
        # Check if the category itself is mentioned
        if category in text:
            detected.add(category)
            
        # Check synonyms
        for word in keywords:
            if word in text:
                detected.add(category)
                break  # Found one match for this category, move to next
    
    # 3. Fallback
    if not detected:
        return ["general"]
        
    return list(detected)