# -*- coding: utf-8 -*-
"""
Clinic Finder Module
Finds and returns nearby clinics based on user location
"""

import json
from typing import Optional


def load_clinics() -> dict:
    """Load clinic data from JSON file"""
    try:
        with open('data/clinics.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def check_for_clinic_request(text: str) -> bool:
    """Check if user is requesting clinic information"""
    clinic_keywords = [
        'clinic', 'hospital', 'doctor', 'clinic chahiye', 'doctor dikhaana',
        'najdeeki', 'nearby', 'paas mein', 'clinic dhundo', 'hospital kahan'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in clinic_keywords)


def extract_location(text: str) -> Optional[str]:
    """Extract location from user input"""
    # Simple location extraction - looks for common patterns
    # In production, you'd use NER or location API
    
    # Remove common words
    words = text.split()
    location_words = []
    
    skip_words = ['mein', 'ka', 'ki', 'hai', 'hain', 'the', 'in', 'at', 'near']
    
    for word in words:
        if word.lower() not in skip_words and len(word) > 2:
            location_words.append(word)
    
    if location_words:
        return ' '.join(location_words[:3])  # Take first few words as location
    
    return None


def find_nearby_clinics(location: str, language: str) -> str:
    """Find and return nearby clinics based on location"""
    clinics = load_clinics()
    location_lower = location.lower()
    
    # Search in clinic database
    matching_clinics = []
    for area, clinic_list in clinics.items():
        if area.lower() in location_lower or location_lower in area.lower():
            matching_clinics = clinic_list
            break
    
    if not matching_clinics:
        # No clinics found
        responses = {
            'hindi': f"""
Maaf kijiye, mere database mein "{location}" ke liye clinic information nahi hai.

**Aap ye kar sakte hain:**
• Google Maps par "clinic near me" search karein
• Local hospital ka helpline number call karein
• Kisi aur najdeeki area ka naam try karein

Ya fir doctor ko urgent dekhna hai toh:
• Najdeeki government hospital jayein
• 108 (Ambulance/Health helpline) dial karein

Koi aur area ka naam bataana chahenge?
""",
            'english': f"""
Sorry, I don't have clinic information for "{location}" in my database.

**You can try:**
• Search "clinic near me" on Google Maps
• Call local hospital helpline
• Try a different nearby area name

If urgent doctor visit needed:
• Visit nearest government hospital
• Dial 108 (Ambulance/Health helpline)

Would you like to try a different area?
"""
        }
        return responses.get(language, responses['hindi'])
    
    # Format clinic information
    clinic_text = ""
    
    if language == 'hindi':
        clinic_text = f"**{location} ke najdeeki clinics:**\n\n"
        for i, clinic in enumerate(matching_clinics[:3], 1):
            clinic_text += f"{i}. **{clinic['name']}**\n"
            clinic_text += f"   📍 Address: {clinic['address']}\n"
            if 'timing' in clinic:
                clinic_text += f"   🕐 Timing: {clinic['timing']}\n"
            if 'phone' in clinic:
                clinic_text += f"   📞 Phone: {clinic['phone']}\n"
            clinic_text += "\n"
        
        clinic_text += "**Yaad rakhein:** Jaane se pehle ek baar phone kar lein.\n"
    else:
        clinic_text = f"**Nearby clinics in {location}:**\n\n"
        for i, clinic in enumerate(matching_clinics[:3], 1):
            clinic_text += f"{i}. **{clinic['name']}**\n"
            clinic_text += f"   📍 Address: {clinic['address']}\n"
            if 'timing' in clinic:
                clinic_text += f"   🕐 Timing: {clinic['timing']}\n"
            if 'phone' in clinic:
                clinic_text += f"   📞 Phone: {clinic['phone']}\n"
            clinic_text += "\n"
        
        clinic_text += "**Remember:** Please call before visiting.\n"
    
    return clinic_text
