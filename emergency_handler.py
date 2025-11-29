# -*- coding: utf-8 -*-
"""
Emergency Detection and Response Module
Handles emergency situations and provides immediate alerts
"""

def detect_emergency(text: str) -> bool:
    """
    Detect emergency keywords in user input
    Returns: True if emergency detected
    """
    emergency_keywords = {
        'hindi': [
            'chest pain', 'seene mein dard', 'dil ka dard', 'saans nahi aa rahi',
            'bahut bleeding', 'khoon bah raha', 'behosh', 'accident',
            'stroke', 'paralysis', 'lakwa', 'heart attack'
        ],
        'english': [
            'chest pain', 'heart attack', 'can\'t breathe', 'breathing difficulty',
            'heavy bleeding', 'fainting', 'fainted', 'severe accident',
            'stroke', 'paralysis', 'unconscious'
        ]
    }
    
    text_lower = text.lower()
    
    for lang in emergency_keywords:
        for keyword in emergency_keywords[lang]:
            if keyword in text_lower:
                return True
    
    return False


def get_emergency_response(language: str) -> str:
    """Generate emergency response message"""
    responses = {
        'hindi': """
🚨 YEH EMERGENCY JAISA LAG RAHA HAI!

KRIPYA TURANT:
✅ Apne najdeeki hospital ya emergency service se sampark karein
✅ 108 (Ambulance) dial karein
✅ Kisi ko saath mein rakhein

Agar sambhav ho toh turant hospital jayein. Der na karein!
""",
        'english': """
🚨 THIS SEEMS LIKE AN EMERGENCY!

PLEASE IMMEDIATELY:
✅ Contact your nearest hospital or emergency service
✅ Call 108 (Ambulance)
✅ Have someone stay with you

If possible, go to the hospital right away. Don't delay!
"""
    }
    
    return responses.get(language, responses['hindi'])
