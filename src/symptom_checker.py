# -*- coding: utf-8 -*-
"""
Symptom Detection and Analysis Module
Extracts symptoms from user input and provides appropriate guidance
"""

from typing import List


def extract_symptoms(text: str) -> List[str]:
    """Extract common symptoms from user input across all 8 languages"""
    symptom_keywords = {
        'headache': [
            # Hindi/Hinglish
            'sir dard', 'headache', 'head pain', 'sar dard',
            # Marathi
            'डोकेदुखी', 'dokedhukhi',
            # Bengali
            'মাথা ব্যথা', 'matha byatha',
            # Tamil
            'தலைவலி', 'thalaivirai',
            # Telugu
            'తలనొప్పి', 'thalanoppi',
            # Punjabi
            'ਸਿਰ ਦਰਦ', 'sir darad',
            # Gujarati
            'માથાનો દુખાવો', 'mathano dukhavo'
        ],
        'fever': [
            # Hindi/Hinglish
            'bukhar', 'fever', 'tap', 'badan garam',
            # Marathi
            'ताप', 'taap',
            # Bengali
            'জ্বর', 'jvar',
            # Tamil
            'காய்ச்சல்', 'kaychhal',
            # Telugu
            'జ్వరం', 'jvaram',
            # Punjabi
            'ਬੁਖ਼ਾਰ', 'bukhar',
            # Gujarati
            'તાવ', 'tav'
        ],
        'cough': [
            # Hindi/Hinglish
            'khansi', 'cough', 'khaansi',
            # Marathi
            'खोकला', 'khokala',
            # Bengali
            'কাশি', 'kashi',
            # Tamil
            'இருமல்', 'irumal',
            # Telugu
            'దగ్గు', 'daggu',
            # Punjabi
            'ਖੰਘ', 'khangh',
            # Gujarati
            'ઉધરસ', 'udharas'
        ],
        'cold': [
            # Hindi/Hinglish
            'sardi', 'cold', 'zukam', 'nazla',
            # Marathi
            'सर्दी', 'sardhi',
            # Bengali
            'সর্দি', 'sardi',
            # Tamil
            'சளி', 'chazhi',
            # Telugu
            'జలుబు', 'jalabu',
            # Punjabi
            'ਜ਼ੁਕਾਮ', 'zukam',
            # Gujarati
            'શરદી', 'shardi'
        ],
        'stomach_pain': [
            # Hindi/Hinglish
            'pet dard', 'stomach pain', 'pet mein dard', 'paet dard',
            # Marathi
            'पोटदुखी', 'potdukhi',
            # Bengali
            'পেট ব্যথা', 'pet byatha',
            # Tamil
            'வயிற்று வலி', 'vayitru vali',
            # Telugu
            'కడుపు నొప్పి', 'kadapu noppi',
            # Punjabi
            'ਪੇਟ ਦਰਦ', 'pet darad',
            # Gujarati
            'પેટમાં દુખાવો', 'petman dukhavo'
        ],
        'vomiting': [
            # Hindi/Hinglish
            'ulti', 'vomit', 'vomiting', 'qai',
            # Marathi
            'उलटी', 'oolti',
            # Bengali
            'বমি', 'bomi',
            # Tamil
            'வாந்தி', 'vanthi',
            # Telugu
            'వాంతులు', 'vantulu',
            # Punjabi
            'ਉਲਟੀ', 'ulti',
            # Gujarati
            'ઉલટી', 'ulti'
        ],
        'diarrhea': [
            # Hindi/Hinglish
            'dast', 'loose motion', 'diarrhea', 'patla pakhana',
            # Marathi
            'जुलाब', 'julab',
            # Bengali
            'ডায়রিয়া', 'diarrhea',
            # Tamil
            'வயிற்றுப்போக்கு', 'vairuppokku',
            # Telugu
            'విరేచనాలు', 'virechanalu',
            # Punjabi
            'ਦਸਤ', 'dast',
            # Gujarati
            'ઝાડા', 'jhada'
        ],
        'body_pain': [
            # Hindi/Hinglish
            'badan dard', 'body pain', 'body ache', 'sharir dard',
            # Marathi
            'शरीर दुखणे', 'sharir dukhane',
            # Bengali
            'শরীর ব্যথা', 'shorir byatha',
            # Tamil
            'உடல் வலி', 'udal vali',
            # Telugu
            'శరీర నొప్పి', 'sharira noppi',
            # Punjabi
            'ਸਰੀਰ ਦਰਦ', 'sharir darad',
            # Gujarati
            'શરીરમાં દુખાવો', 'sharirman dukhavo'
        ],
        'weakness': [
            # Hindi/Hinglish
            'kamzori', 'weakness', 'thakan', 'fatigue',
            # Marathi
            'अशक्तपणा', 'ashaktapana',
            # Bengali
            'দুর্বলতা', 'durbalata',
            # Tamil
            'பலவீனம்', 'palaveenam',
            # Telugu
            'బలహీనత', 'balaheenatha',
            # Punjabi
            'ਕਮਜ਼ੋਰੀ', 'kamzori',
            # Gujarati
            'નબળાઈ', 'nablai'
        ]
    }
    
    text_lower = text.lower()
    detected_symptoms = []
    
    for symptom, keywords in symptom_keywords.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                detected_symptoms.append(symptom)
                break
    
    return detected_symptoms
