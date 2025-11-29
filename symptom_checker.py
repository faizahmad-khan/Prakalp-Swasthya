# -*- coding: utf-8 -*-
"""
Symptom Detection and Analysis Module
Extracts symptoms from user input and provides appropriate guidance
"""

from typing import List


def extract_symptoms(text: str) -> List[str]:
    """Extract common symptoms from user input"""
    symptom_keywords = {
        'headache': ['sir dard', 'headache', 'head pain', 'sar dard'],
        'fever': ['bukhar', 'fever', 'tap', 'badan garam'],
        'cough': ['khansi', 'cough', 'khaansi'],
        'cold': ['sardi', 'cold', 'zukam', 'nazla'],
        'stomach_pain': ['pet dard', 'stomach pain', 'pet mein dard', 'paet dard'],
        'vomiting': ['ulti', 'vomit', 'vomiting', 'qai'],
        'diarrhea': ['dast', 'loose motion', 'diarrhea', 'patla pakhana'],
        'body_pain': ['badan dard', 'body pain', 'body ache', 'sharir dard'],
        'weakness': ['kamzori', 'weakness', 'thakan', 'fatigue']
    }
    
    text_lower = text.lower()
    detected_symptoms = []
    
    for symptom, keywords in symptom_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected_symptoms.append(symptom)
                break
    
    return detected_symptoms
