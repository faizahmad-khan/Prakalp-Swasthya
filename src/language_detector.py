# -*- coding: utf-8 -*-
"""
Enhanced Language Detection Module
Detects user's language from input text with support for 8 Indian languages
Supports: Hindi, English, Marathi, Bengali, Tamil, Telugu, Punjabi, Gujarati
"""

import re
from typing import Dict, List


def detect_language(text: str) -> str:
    """
    Detect the language of user input using script detection and keyword matching
    Returns: Language code (hindi, english, marathi, bengali, tamil, telugu, punjabi, gujarati)
    """
    if not text or len(text.strip()) == 0:
        return 'hindi'  # Default to Hindi
    
    # First, try script-based detection (most reliable)
    script_lang = detect_by_script(text)
    if script_lang:
        return script_lang
    
    # Fallback to keyword-based detection for Romanized text (Hinglish)
    return detect_by_keywords(text)


def detect_by_script(text: str) -> str:
    """
    Detect language based on Unicode script ranges
    Very accurate for non-Romanized text
    """
    # Count characters in each script
    script_counts = {
        'devanagari': 0,  # Hindi/Marathi
        'bengali': 0,
        'tamil': 0,
        'telugu': 0,
        'gurmukhi': 0,  # Punjabi
        'gujarati': 0,
        'latin': 0  # English
    }
    
    for char in text:
        code = ord(char)
        
        # Devanagari (Hindi/Marathi): U+0900 to U+097F
        if 0x0900 <= code <= 0x097F:
            script_counts['devanagari'] += 1
        
        # Bengali: U+0980 to U+09FF
        elif 0x0980 <= code <= 0x09FF:
            script_counts['bengali'] += 1
        
        # Gurmukhi (Punjabi): U+0A00 to U+0A7F
        elif 0x0A00 <= code <= 0x0A7F:
            script_counts['gurmukhi'] += 1
        
        # Gujarati: U+0A80 to U+0AFF
        elif 0x0A80 <= code <= 0x0AFF:
            script_counts['gujarati'] += 1
        
        # Tamil: U+0B80 to U+0BFF
        elif 0x0B80 <= code <= 0x0BFF:
            script_counts['tamil'] += 1
        
        # Telugu: U+0C00 to U+0C7F
        elif 0x0C00 <= code <= 0x0C7F:
            script_counts['telugu'] += 1
        
        # Latin (English): U+0041 to U+007A
        elif (0x0041 <= code <= 0x005A) or (0x0061 <= code <= 0x007A):
            script_counts['latin'] += 1
    
    # Find the script with maximum count
    max_script = max(script_counts, key=script_counts.get)
    max_count = script_counts[max_script]
    
    # Require at least 3 characters in the detected script
    if max_count >= 3:
        if max_script == 'devanagari':
            # Differentiate between Hindi and Marathi using keywords
            return differentiate_hindi_marathi(text)
        elif max_script == 'bengali':
            return 'bengali'
        elif max_script == 'tamil':
            return 'tamil'
        elif max_script == 'telugu':
            return 'telugu'
        elif max_script == 'gurmukhi':
            return 'punjabi'
        elif max_script == 'gujarati':
            return 'gujarati'
        elif max_script == 'latin':
            return 'english'
    
    return None


def differentiate_hindi_marathi(text: str) -> str:
    """
    Differentiate between Hindi and Marathi (both use Devanagari script)
    Uses language-specific keywords
    """
    text_lower = text.lower()
    
    # Marathi-specific markers
    marathi_markers = ['आहे', 'आहेत', 'होते', 'होती', 'मी', 'तुम्ही', 'तुमचा', 'माझा', 
                       'नाही', 'काय', 'कसे', 'कुठे', 'aahe', 'aahes', 'mi', 'tumhi']
    
    # Hindi-specific markers  
    hindi_markers = ['है', 'हैं', 'था', 'थी', 'मैं', 'आप', 'आपका', 'मेरा',
                     'नहीं', 'क्या', 'कैसे', 'कहाँ', 'hain', 'main', 'aap']
    
    marathi_count = sum(1 for marker in marathi_markers if marker in text_lower)
    hindi_count = sum(1 for marker in hindi_markers if marker in text_lower)
    
    if marathi_count > hindi_count:
        return 'marathi'
    else:
        return 'hindi'


def detect_by_keywords(text: str) -> str:
    """
    Detect language using common keywords and patterns
    Used for Romanized/transliterated text (Hinglish, etc.)
    """
    text_lower = text.lower()
    
    # Language-specific keyword patterns with weights
    language_patterns = {
        'hindi': {
            'patterns': ['hai', 'hain', 'mujhe', 'kya', 'aap', 'ko', 'se', 'mein', 
                        'ka', 'ki', 'ho', 'thi', 'tha', 'main', 'aapko', 'mere',
                        'tumhe', 'usko', 'yeh', 'woh', 'kaise', 'kahan', 'kab',
                        'bukhar', 'dard', 'sir', 'pet', 'doctor', 'clinic'],
            'weight': 1
        },
        'english': {
            'patterns': ['the', 'is', 'are', 'was', 'were', 'what', 'how', 'can', 
                        'have', 'has', 'with', 'for', 'from', 'this', 'that',
                        'my', 'your', 'his', 'her', 'their', 'pain', 'fever',
                        'headache', 'stomach', 'doctor', 'clinic', 'need', 'help'],
            'weight': 1
        },
        'marathi': {
            'patterns': ['aahe', 'aahes', 'aahot', 'mi', 'tumhi', 'tu', 'tyala',
                        'mala', 'tula', 'kay', 'kase', 'kuthe', 'kev', 'asa'],
            'weight': 1.2
        },
        'bengali': {
            'patterns': ['ami', 'tumi', 'apni', 'amar', 'tomar', 'apnar',
                        'ki', 'keno', 'kothay', 'kivabe', 'ache', 'chhilo'],
            'weight': 1.2
        },
        'tamil': {
            'patterns': ['nan', 'nee', 'neenga', 'enna', 'eppadi', 'enga',
                        'ennoda', 'ungala', 'iruku', 'irundu'],
            'weight': 1.2
        },
        'telugu': {
            'patterns': ['nenu', 'nuvvu', 'meeru', 'naa', 'nee', 'mee',
                        'enti', 'ela', 'ekkada', 'undi', 'unnadi'],
            'weight': 1.2
        },
        'punjabi': {
            'patterns': ['main', 'tu', 'tusi', 'mera', 'tera', 'tusada',
                        'ki', 'kivein', 'kithe', 'hai', 'hain', 'si'],
            'weight': 1.2
        },
        'gujarati': {
            'patterns': ['hu', 'tame', 'tu', 'maru', 'taru', 'tamaru',
                        'shu', 'kem', 'kyaa', 'chhe', 'hato', 'hati'],
            'weight': 1.2
        }
    }
    
    # Count matches for each language
    scores = {}
    for lang, data in language_patterns.items():
        count = 0
        for pattern in data['patterns']:
            # Use word boundaries to avoid partial matches
            if re.search(r'\b' + re.escape(pattern) + r'\b', text_lower):
                count += 1
        scores[lang] = count * data['weight']
    
    # Get language with highest score
    if scores:
        max_lang = max(scores, key=scores.get)
        max_score = scores[max_lang]
        
        # Require at least 2 matches to confirm language
        if max_score >= 2:
            return max_lang
    
    # Default to Hindi for Indian context
    return 'hindi'


def get_language_name(lang_code: str) -> str:
    """
    Get the full language name from language code
    """
    language_names = {
        'hindi': 'Hindi (हिंदी)',
        'english': 'English',
        'marathi': 'Marathi (मराठी)',
        'bengali': 'Bengali (বাংলা)',
        'tamil': 'Tamil (தமிழ்)',
        'telugu': 'Telugu (తెలుగు)',
        'punjabi': 'Punjabi (ਪੰਜਾਬੀ)',
        'gujarati': 'Gujarati (ગુજરાતી)'
    }
    return language_names.get(lang_code, 'Hindi')
