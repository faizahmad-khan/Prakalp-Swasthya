# -*- coding: utf-8 -*-
"""
Clinic Finder Module
Finds and returns nearby clinics based on user location
Uses PostgreSQL database with JSON file fallback
"""

import json
import logging
from typing import Optional, List
from pathlib import Path

try:
    from sqlalchemy import or_ as sql_or
except ImportError:
    sql_or = None

logger = logging.getLogger(__name__)

# Database imports are optional - moved inside functions to handle gracefully
try:
    from database import get_db_manager, Clinic
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    logger.warning("Database module not available - clinic search will use fallback")

# Load clinics from JSON file
CLINICS_DATA = None

def load_clinics_json():
    """Load clinics data from JSON file"""
    global CLINICS_DATA
    if CLINICS_DATA is not None:
        return CLINICS_DATA
    
    try:
        # Try multiple possible paths
        json_paths = [
            Path('data/clinics.json'),
            Path('clinics.json'),
            Path('../data/clinics.json')
        ]
        
        for json_path in json_paths:
            if json_path.exists():
                with open(json_path, 'r', encoding='utf-8') as f:
                    CLINICS_DATA = json.load(f)
                    logger.info(f"Loaded clinics data from {json_path}")
                    return CLINICS_DATA
        
        logger.warning("Could not find clinics.json file")
        CLINICS_DATA = {}
        return CLINICS_DATA
    except Exception as e:
        logger.error(f"Error loading clinics.json: {e}")
        CLINICS_DATA = {}
        return CLINICS_DATA


def check_for_clinic_request(text: str) -> bool:
    """Check if user is requesting clinic information"""
    clinic_keywords = [
        'clinic', 'hospital', 'doctor', 'clinic chahiye', 'doctor dikhaana',
        'najdeeki', 'nearby', 'paas mein', 'clinic dhundo', 'hospital kahan',
        'pharmacy', 'medical', 'chemist', 'dispensary'
    ]
    
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in clinic_keywords)


def extract_location(text: str) -> Optional[str]:
    """Extract location from user input"""
    # Simple location extraction - looks for common patterns
    # In production, you'd use NER or location API
    
    # Clean the input
    text = text.strip()
    
    # If input is a location key format (e.g., "Lucknow_Gomti_Nagar_Patrakarpuram")
    if '_' in text and text.replace('_', '').replace(' ', '').isalnum():
        logger.info(f"Detected location key format: {text}")
        return text
    
    # If input is a pincode (6 digits), return as is
    if text.isdigit() and len(text) == 6:
        logger.info(f"Detected pincode: {text}")
        return text
    
    # Remove common filler words but keep location-related terms
    words = text.split()
    location_words = []
    
    skip_words = [
        'mein', 'ka', 'ki', 'hai', 'hain', 'the', 'in', 'at', 'me', 
        'please', 'kripya', 'se', 'batayen', 'batao', 'bataye', 'tell',
        'my', 'is', 'area', 'location', 'jagah', 'city', 'shahar'
    ]
    
    for word in words:
        cleaned_word = word.strip('.,!?;:')
        if cleaned_word.lower() not in skip_words and len(cleaned_word) > 2:
            location_words.append(cleaned_word)
    
    if location_words:
        # Join extracted words (up to 3 words for compound locations)
        location = ' '.join(location_words[:3])
        
        # Validate: Don't accept text that looks like a symptom description
        symptom_indicators = ['hai', 'ho', 'raha', 'gaya', 'feeling', 'have', 'got', 
                             'mujhe', 'mera', 'my', 'me', 'dard', 'pain', 'ache']
        if any(indicator in location.lower() for indicator in symptom_indicators):
            logger.info(f"Rejected as location (looks like symptom): {location}")
            return None
        
        logger.info(f"Extracted location: {location}")
        return location
    
    # Don't blindly return any input as location - this causes false matches
    # Only very specific patterns should reach here
    return None


def search_clinics_in_json(location: str, limit: int = 10) -> List[dict]:
    """
    Search for clinics in JSON file
    
    Args:
        location: Location string to search for
        limit: Maximum number of clinics to return
    
    Returns:
        List of clinic dictionaries
    """
    clinics_data = load_clinics_json()
    if not clinics_data:
        return []
    
    location_clean = location.strip()
    matching_clinics = []
    
    # Strategy 1: Exact location key match (e.g., "Lucknow_Gomti_Nagar_Patrakarpuram")
    if location_clean in clinics_data:
        logger.info(f"Found exact location key match: {location_clean}")
        matching_clinics = clinics_data[location_clean]
        return matching_clinics[:limit]
    
    # Strategy 2: Partial match in location keys (case-insensitive)
    location_lower = location_clean.lower()
    for location_key, clinics in clinics_data.items():
        if location_lower in location_key.lower():
            logger.info(f"Found partial match in key: {location_key}")
            matching_clinics.extend(clinics)
    
    if matching_clinics:
        return matching_clinics[:limit]
    
    # Strategy 3: Search in clinic addresses and names (for pincode or area name)
    for location_key, clinics in clinics_data.items():
        for clinic in clinics:
            # Check if location appears in address or name
            if (location_lower in clinic.get('address', '').lower() or
                location_lower in clinic.get('name', '').lower()):
                if clinic not in matching_clinics:  # Avoid duplicates
                    matching_clinics.append(clinic)
    
    return matching_clinics[:limit]


def search_clinics_in_db(location: str, limit: int = 5) -> List[dict]:
    """
    Search for clinics in PostgreSQL database
    
    Args:
        location: Location string to search for
        limit: Maximum number of clinics to return
    
    Returns:
        List of clinic dictionaries
    """
    if not DB_AVAILABLE or sql_or is None:
        logger.warning("Database not available for clinic search")
        return []
    
    try:
        db_manager = get_db_manager()
        
        with db_manager.get_session() as session:
            # Clean location string
            location_clean = location.strip().lower()
            
            # Search in multiple fields
            search_term = f"%{location_clean}%"
            
            clinics = session.query(Clinic).filter(
                sql_or(
                    Clinic.city.ilike(search_term),
                    Clinic.area.ilike(search_term),
                    Clinic.location_key.ilike(search_term),
                    Clinic.address.ilike(search_term)
                ),
                Clinic.is_active == True
            ).limit(limit).all()
            
            # Return list of clinic dictionaries
            return [clinic.to_dict() for clinic in clinics]
    
    except Exception as e:
        logger.error(f"Error searching clinics in database: {e}")
        return []


def find_nearby_clinics(location: str, language: str) -> str:
    """Find and return nearby clinics based on location"""
    
    # First, try database search
    matching_clinics = search_clinics_in_db(location, limit=10)
    
    # If database is empty or unavailable, use JSON fallback
    if not matching_clinics:
        logger.info("Database search returned no results, trying JSON fallback")
        matching_clinics = search_clinics_in_json(location, limit=10)
    
    if not matching_clinics:
        # No clinics found
        responses = {
            'hinglish': f"""
Sorry, mere database mein "{location}" ke liye clinic information nahi hai.

**Aap ye kar sakte hain:**
• Location key format mein try karein (jaise: Lucknow_Gomti_Nagar_Patrakarpuram)
• Sirf area naam dijiye (jaise: Patrakarpuram, Gomti Nagar)
• Pincode dijiye (jaise: 226010)
• Google Maps par "clinic near me" search karein
• Local hospital ka helpline number call karein

Ya fir doctor ko urgent dekhna hai toh:
• Najdeeki government hospital jayein
• 108 (Ambulance/Health helpline) dial karein

Koi aur location try karna chahenge?
""",
            'hindi': f"""
Maaf kijiye, mere database mein "{location}" ke liye clinic information nahi hai.

**Aap ye kar sakte hain:**
• Location key format mein try karein (jaise: Lucknow_Gomti_Nagar_Patrakarpuram)
• Sirf area naam dijiye (jaise: Patrakarpuram, Gomti Nagar)
• Pincode dijiye (jaise: 226010)
• Google Maps par "clinic near me" search karein
• Local hospital ka helpline number call karein

Ya fir doctor ko urgent dekhna hai toh:
• Najdeeki government hospital jayein
• 108 (Ambulance/Health helpline) dial karein

Koi aur location format try karna chahenge?
""",
            'english': f"""
Sorry, I don't have clinic information for "{location}" in my database.

**You can try:**
• Location key format (e.g., Lucknow_Gomti_Nagar_Patrakarpuram)
• Just the area name (e.g., Patrakarpuram, Gomti Nagar)
• Pincode (e.g., 226010)
• Search "clinic near me" on Google Maps
• Call local hospital helpline

If urgent doctor visit needed:
• Visit nearest government hospital
• Dial 108 (Ambulance/Health helpline)

Would you like to try a different area?
""",
            'marathi': f"""
माफ करा, माझ्या डेटाबेसमध्ये "{location}" साठी क्लिनिक माहिती नाही.

**तुम्ही हे करू शकता:**
• Google Maps वर "clinic near me" शोधा
• स्थानिक रुग्णालयाच्या हेल्पलाइनवर कॉल करा
• दुसऱ्या जवळच्या क्षेत्राचे नाव वापरून पहा

जर तातडीने डॉक्टरांना भेटणे आवश्यक असल्यास:
• जवळच्या सरकारी रुग्णालयात जा
• 108 (रुग्णवाहिका/आरोग्य हेल्पलाइन) डायल करा

दुसरे क्षेत्र सांगू इच्छिता का?
""",
            'bengali': f"""
দুঃখিত, আমার ডেটাবেসে "{location}" এর জন্য ক্লিনিক তথ্য নেই।

**আপনি চেষ্টা করতে পারেন:**
• Google Maps-এ "clinic near me" অনুসন্ধান করুন
• স্থানীয় হাসপাতালের হেল্পলাইনে কল করুন
• অন্য কাছাকাছি এলাকার নাম চেষ্টা করুন

জরুরি ডাক্তারের দর্শন প্রয়োজন হলে:
• নিকটতম সরকারি হাসপাতালে যান
• 108 (অ্যাম্বুলেন্স/স্বাস্থ্য হেল্পলাইন) ডায়াল করুন

অন্য এলাকার নাম বলতে চান?
""",
            'tamil': f"""
மன்னிக்கவும், எனது தரவுத்தளத்தில் "{location}" க்கான கிளினிக் தகவல் இல்லை.

**நீங்கள் முயற்சி செய்யலாம்:**
• Google Maps இல் "clinic near me" தேடுங்கள்
• உள்ளூர் மருத்துவமனை ஹெல்ப்லைனை அழைக்கவும்
• வேறு அருகிலுள்ள பகுதி பெயரை முயற்சிக்கவும்

அவசர மருத்துவர் பார்வை தேவைப்பட்டால்:
• அருகிலுள்ள அரசு மருத்துவமனைக்கு செல்லுங்கள்
• 108 (ஆம்புலன்ஸ்/உடல்நலம் ஹெல்ப்லைன்) டயல் செய்யுங்கள்

வேறு பகுதி பெயரை சொல்ல விரும்புகிறீர்களா?
""",
            'telugu': f"""
క్షమించండి, నా డేటాబేస్‌లో "{location}" కోసం క్లినిక్ సమాచారం లేదు.

**మీరు ప్రయత్నించవచ్చు:**
• Google Maps లో "clinic near me" వెతకండి
• స్థానిక హాస్పిటల్ హెల్ప్‌లైన్‌కు కాల్ చేయండి
• వేరొక సమీప ప్రాంతం పేరును ప్రయత్నించండి

అత్యవసర వైద్యుడు అవసరమైతే:
• సమీప ప్రభుత్వ ఆసుపత్రికి వెళ్లండి
• 108 (అంబులెన్స్/ఆరోగ్య హెల్ప్‌లైన్) డయల్ చేయండి

వేరే ప్రాంతం పేరు చెప్పాలనుకుంటున్నారా?
""",
            'punjabi': f"""
ਮਾਫ਼ ਕਰਨਾ, ਮੇਰੇ ਡੇਟਾਬੇਸ ਵਿੱਚ "{location}" ਲਈ ਕਲੀਨਿਕ ਜਾਣਕਾਰੀ ਨਹੀਂ ਹੈ।

**ਤੁਸੀਂ ਕੋਸ਼ਿਸ਼ ਕਰ ਸਕਦੇ ਹੋ:**
• Google Maps ਤੇ "clinic near me" ਖੋਜੋ
• ਸਥਾਨਕ ਹਸਪਤਾਲ ਦੀ ਹੈਲਪਲਾਈਨ ਤੇ ਕਾਲ ਕਰੋ
• ਕਿਸੇ ਹੋਰ ਨੇੜਲੇ ਖੇਤਰ ਦਾ ਨਾਮ ਵਰਤ ਕੇ ਦੇਖੋ

ਜੇ ਤੁਰੰਤ ਡਾਕਟਰ ਨੂੰ ਮਿਲਣ ਦੀ ਲੋੜ ਹੋਵੇ:
• ਨੇੜਲੇ ਸਰਕਾਰੀ ਹਸਪਤਾਲ ਜਾਓ
• 108 (ਐਂਬੂਲੈਂਸ/ਸਿਹਤ ਹੈਲਪਲਾਈਨ) ਡਾਇਲ ਕਰੋ

ਹੋਰ ਖੇਤਰ ਦਾ ਨਾਮ ਦੱਸਣਾ ਚਾਹੁੰਦੇ ਹੋ?
""",
            'gujarati': f"""
માફ કરશો, મારા ડેટાબેઝમાં "{location}" માટે ક્લિનિક માહિતી નથી.

**તમે પ્રયાસ કરી શકો છો:**
• Google Maps પર "clinic near me" શોધો
• સ્થાનિક હોસ્પિટલની હેલ્પલાઇનને કૉલ કરો
• બીજા નજીકના વિસ્તારનું નામ અજમાવો

જો તાત્કાલિક ડૉક્ટરની મુલાકાત જરૂરી હોય:
• નજીકની સરકારી હોસ્પિટલમાં જાઓ
• 108 (એમ્બ્યુલન્સ/આરોગ્ય હેલ્પલાઇન) ડાયલ કરો

બીજા વિસ્તારનું નામ કહેવા માંગો છો?
"""
        }
        return responses.get(language, responses['hindi'])
    
    # Format clinic information
    language_headers = {
        'hinglish': {
            'title': f"**{location} ke najdeeki clinics:**\n\n",
            'address': "📍 Address",
            'timing': "🕐 Timing",
            'phone': "📞 Phone",
            'footer': "**Yaad rakhein:** Jaane se pehle phone kar lein.\n"
        },
        'hindi': {
            'title': f"**{location} ke najdeeki clinics:**\n\n",
            'address': "📍 Address",
            'timing': "🕐 Timing",
            'phone': "📞 Phone",
            'footer': "**Yaad rakhein:** Jaane se pehle ek baar phone kar lein.\n"
        },
        'english': {
            'title': f"**Nearby clinics in {location}:**\n\n",
            'address': "📍 Address",
            'timing': "🕐 Timing",
            'phone': "📞 Phone",
            'footer': "**Remember:** Please call before visiting.\n"
        },
        'marathi': {
            'title': f"**{location} मधील जवळपासचे क्लिनिक:**\n\n",
            'address': "📍 पत्ता",
            'timing': "🕐 वेळ",
            'phone': "📞 फोन",
            'footer': "**लक्षात ठेवा:** जाण्यापूर्वी फोन करा.\n"
        },
        'bengali': {
            'title': f"**{location} এর কাছাকাছি ক্লিনিক:**\n\n",
            'address': "📍 ঠিকানা",
            'timing': "🕐 সময়",
            'phone': "📞 ফোন",
            'footer': "**মনে রাখবেন:** যাওয়ার আগে ফোন করুন।\n"
        },
        'tamil': {
            'title': f"**{location} அருகிலுள்ள கிளினிக்குகள்:**\n\n",
            'address': "📍 முகவரி",
            'timing': "🕐 நேரம்",
            'phone': "📞 தொலைபேசி",
            'footer': "**நினைவில் கொள்ளுங்கள்:** செல்வதற்கு முன் அழைக்கவும்.\n"
        },
        'telugu': {
            'title': f"**{location} సమీప క్లినిక్‌లు:**\n\n",
            'address': "📍 చిరునామా",
            'timing': "🕐 సమయం",
            'phone': "📞 ఫోన్",
            'footer': "**గుర్తుంచుకోండి:** వెళ్లే ముందు ఫోన్ చేయండి.\n"
        },
        'punjabi': {
            'title': f"**{location} ਦੇ ਨੇੜਲੇ ਕਲੀਨਿਕ:**\n\n",
            'address': "📍 ਪਤਾ",
            'timing': "🕐 ਸਮਾਂ",
            'phone': "📞 ਫ਼ੋਨ",
            'footer': "**ਯਾਦ ਰੱਖੋ:** ਜਾਣ ਤੋਂ ਪਹਿਲਾਂ ਫ਼ੋਨ ਕਰੋ।\n"
        },
        'gujarati': {
            'title': f"**{location} નજીકની ક્લિનિક:**\n\n",
            'address': "📍 સરનામું",
            'timing': "🕐 સમય",
            'phone': "📞 ફોન",
            'footer': "**યાદ રાખો:** જતા પહેલા ફોન કરો.\n"
        }
    }
    
    headers = language_headers.get(language, language_headers['hinglish'])
    
    # Show message about number of results
    num_clinics = len(matching_clinics)
    if language == 'hinglish':
        clinic_text = f"**{location} ke najdeeki {num_clinics} clinics mil gaye:**\n\n"
    elif language == 'hindi':
        clinic_text = f"**{location} ke najdeeki {num_clinics} clinics mil gaye:**\n\n"
    else:
        clinic_text = f"**Found {num_clinics} nearby clinics in {location}:**\n\n"
    
    # Show all matching clinics (up to limit)
    for i, clinic in enumerate(matching_clinics[:10], 1):
        clinic_text += f"{i}. **{clinic['name']}**\n"
        clinic_text += f"   {headers['address']}: {clinic.get('address', 'N/A')}\n"
        if clinic.get('timing'):
            clinic_text += f"   {headers['timing']}: {clinic['timing']}\n"
        if clinic.get('phone'):
            clinic_text += f"   {headers['phone']}: {clinic['phone']}\n"
        if clinic.get('specialties'):
            specialties = ', '.join(clinic['specialties']) if isinstance(clinic['specialties'], list) else clinic['specialties']
            clinic_text += f"   🏥 Specialties: {specialties}\n"
        if clinic.get('fees'):
            clinic_text += f"   💰 Fees: {clinic['fees']}\n"
        clinic_text += "\n"
    
    clinic_text += headers['footer']
    
    return clinic_text
